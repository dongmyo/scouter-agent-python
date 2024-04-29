import socket
import threading

from scouterx.common.constants.netcafeconstant.netcafeconstants import TCP_AGENT_V2
from scouterx.common.constants.tcpflag import tcpflag
from scouterx.common.logger.logger import info_logger, error_logger
from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.conf.configure import Configure

ac = Configure()
client = None
client_lock = threading.Lock()


class TCPClient:
    def __init__(self):
        self.conn = None
        self.host = ""
        self.port = 0
        self.connection_timeout = 0
        self.so_timeout = 0
        self.local_addr = ""
        self.obj_hash = 0

    def close(self):
        if self.conn:
            self.conn.close()

    def prepare(self):
        self.host = ac.net_collector_ip
        self.port = ac.net_collector_tcp_port
        self.connection_timeout = ac.net_collector_tcp_connection_timeout_ms
        self.so_timeout = ac.net_collector_tcp_so_timeout_ms
        self.obj_hash = ac.obj_hash

        info_logger.info(f"[scouter]tcp prepare {self.host}, {self.port}")
        try:
            self.conn = socket.create_connection((self.host, self.port), self.connection_timeout / 1000)
        except Exception as e:
            error_logger.error(f"[scouter][err]{e}")
            self.conn = None
            return False

        self.local_addr = "127.0.0.1"  # TODO: Update as needed
        return True

    def process(self):
        if not self.conn:
            return None

        out = DataOutputX(self.conn)
        server_addr = ac.net_collector_ip
        server_port = ac.net_collector_tcp_port

        out.write_int32(TCP_AGENT_V2)
        out.write_int32(self.obj_hash)

        while self.obj_hash == ac.obj_hash and server_addr == ac.net_collector_ip and server_port == ac.net_collector_tcp_port:
            self.conn.settimeout(self.so_timeout / 1000)
            in_ = DataInputX(self.conn)
            buff = in_.read_int_bytes()

            in0 = DataInputX(buff)
            cmd = in0.read_string()
            parameter = in0.read_pack()

            out0 = DataOutputX()
            res = handle(cmd, parameter, in_, out0)
            if res:
                out0.write_uint8(tcpflag.HasNEXT)
                pack = DataOutputX().write_pack(res)
                pack_bytes = pack.get_bytes()
                out0.write_int_bytes(pack_bytes)

            out0.write_uint8(tcpflag.NoNEXT)
            self.conn.sendall(out0.get_bytes())
        return None


def get_tcp_client():
    global client
    with client_lock:
        if client is None:
            client = TCPClient()
    return client
