import socket

import numpy

from scouterx.common.constants.netcafeconstant.netcafeconstants import CAFE_MTU, CAFE
from scouterx.common.logger.logger import error_logger
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.util.keygen.keygen import KeyGen


class UDPClient:
    def __init__(self, remote_address, remote_port):
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.udp_max_bytes = 60000
        self.conn = None
        self.open()

    def set_udp_max_bytes(self, max_bytes):
        self.udp_max_bytes = max_bytes

    def open(self):
        if self.conn is not None:
            self.close()

        address = (self.remote_address, self.remote_port)
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.conn.connect(address)
        except Exception as e:
            error_logger.error(f"[scouter] can't set up udp client. {e}")
            raise

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def write_mtu(self, data, packet_size):
        if self.conn is None:
            return False
        pkid = KeyGen.get_instance().next()
        total = len(data) // packet_size + (len(data) % packet_size > 0)
        for num in range(len(data) // packet_size):
            self.write_mtu_sub(pkid, total, num, data[num * packet_size: (num + 1) * packet_size])
        if len(data) % packet_size != 0:
            remainder = len(data) % packet_size
            self.write_mtu_sub(pkid, total, len(data) // packet_size, data[-remainder:])
        return True

    def write_mtu_sub(self, pkid, total, num, data):
        out = DataOutputX()
        out.write(CAFE_MTU)
        out.write_int32(0)  # In deed, this value is objhash.. but i don't use objhash anymore.
        out.write_int64(pkid)
        out.write_int16(numpy.int16(total))
        out.write_int16(numpy.int16(num))
        out.write_blob(data)
        buff = out.get_bytes()
        self.conn.send(buff)

    def send_buffer_list(self, buffer_count, data):
        out = DataOutputX()
        out.write(CAFE_MTU)
        out.write_int16(buffer_count)
        out.write(data)
        send_data = out.get_bytes()
        self.conn.send(send_data)

    def write_buffer(self, buff):
        if self.conn is None:
            return False
        if len(buff) > self.udp_max_bytes:
            return self.write_mtu(buff, self.udp_max_bytes)
        out = DataOutputX()
        out.write(CAFE)
        out.write(buff)
        self.conn.send(out.get_bytes())
        return True

    def write_buffer_list(self, buffer_list):
        if self.conn is None:
            return False
        out = DataOutputX()
        out_count = 0
        for buff in buffer_list:
            buff_len = len(buff)
            if buff_len + out.get_write_size() > self.udp_max_bytes:
                self.send_buffer_list(out_count, out.get_bytes())
                out = DataOutputX()  # Reset output stream
                out_count = 0
            out.write(buff)
            out_count += 1
        if out.get_write_size() > 0:
            self.send_buffer_list(out_count, out.get_bytes())
        return True
