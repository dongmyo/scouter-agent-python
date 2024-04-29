import queue
import threading
import time
from collections import deque

from scouterx.common.factory.channelfactory.channel_factory import ChannelFactory
from scouterx.common.logger.logger import warning_logger, info_logger
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.objectpack import ObjectPack
from scouterx.conf.configure import Configure
from scouterx.netio.udpclient.udpclient import UDPClient

ac = Configure()

udp_obj_hash = 0
server_addr = ""
udp_server_port = 0
udp_max_bytes = 0


class UDPSender:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(UDPSender, cls).__new__(cls)
                cls._instance.initialize()
            return cls._instance

    def initialize(self):
        global server_addr, udp_server_port, udp_max_bytes
        server_addr = ac.net_collector_ip
        udp_server_port = ac.net_collector_udp_port
        udp_max_bytes = ac.udp_max_bytes

        self.udp_channel = ChannelFactory.get_udp_channel()
        self.running = True
        self.udp_client = UDPClient(server_addr, udp_server_port)
        self.udp_client.set_udp_max_bytes(udp_max_bytes)
        threading.Thread(target=self.run).start()
        threading.Thread(target=self.reload_udp_sender).start()

    def reload_udp_sender(self):
        global server_addr, udp_server_port, udp_max_bytes
        while True:
            time.sleep(1)
            if (server_addr != ac.net_collector_ip or
                    udp_server_port != ac.net_collector_udp_port or
                    udp_max_bytes != ac.udp_max_bytes):
                server_addr = ac.net_collector_ip
                udp_server_port = ac.net_collector_udp_port
                udp_max_bytes = ac.udp_max_bytes

                self.running = True
                prev_client = self.udp_client
                self.udp_client = UDPClient(server_addr, udp_server_port)
                self.udp_client.set_udp_max_bytes(udp_max_bytes)

                if prev_client.conn:
                    prev_client.conn.close()

    def add_pack(self, pack):
        out = DataOutputX()
        out.write_pack(pack)
        bytes_ = out.get_bytes()
        try:
            self.udp_channel.put_nowait(bytes_)
        except queue.Full:
            warning_logger.warning("UDP channel is full.")

    def add_buffer(self, buffer):
        try:
            self.udp_channel.put_nowait(buffer)
        except queue.Full:
            warning_logger.warning("UDP channel is full.")

    def send_pack_direct(self, pack):
        if ac.trace_obj_send:
            if isinstance(pack, ObjectPack):
                info_logger.info(f"[scouter] SendPackDirect[ObjPack], to:{self.udp_client.conn.remote_addr}, pack:{pack.to_string()}")
        out = DataOutputX()
        out.write_pack(pack)
        bytes_ = out.get_bytes()
        threading.Thread(target=self.udp_client.write_buffer, args=(bytes_,)).start()

    def send_direct(self, buffer_list):
        if not buffer_list:
            return
        threading.Thread(target=self.send_list, args=(buffer_list,)).start()

    def run(self):
        while self.running:
            size = self.get_queue_size()
            if size == 0:
                time.sleep(0.1)
            elif size == 1:
                p = self.udp_channel.get()
                self.udp_client.write_buffer(p)
            else:
                self.send(size)

    def get_queue_size(self):
        return self.udp_channel.qsize()

    def send(self, size):
        buffer_list = deque()
        bytes_ = 0
        for _ in range(size):
            buffer = self.udp_channel.get()
            if bytes_ + len(buffer) >= ac.udp_max_bytes:
                self.send_list(buffer_list)
                bytes_ = 0
                buffer_list.clear()
            bytes_ += len(buffer)
            buffer_list.append(buffer)
        self.udp_client.write_buffer_list(buffer_list)

    def send_list(self, buffer_list):
        if len(buffer_list) == 0:
            return
        elif len(buffer_list) == 1:
            self.udp_client.write_buffer(buffer_list[0])
        else:
            self.udp_client.write_buffer_list(buffer_list)
