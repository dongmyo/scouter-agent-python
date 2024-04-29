import unittest
import time

from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.perfcounterpack import PerfCounterPack
from scouterx.netio.udpclient.udpclient import UDPClient


class TestUDPClient(unittest.TestCase):
    def test_udp_client(self):
        udp_client = UDPClient('127.0.0.1', 6100)
        perf_pack = PerfCounterPack()
        perf_pack.put("abd", 123)
        perf_pack.obj_name = "testObj"
        perf_pack.time = int(time.time())
        perf_pack.time_type = "REALTIME"  # Assuming we have a corresponding constant or just use the string
        out = DataOutputX()
        out.write_pack(perf_pack)
        udp_client.write_buffer(out.get_bytes())

    def test_multi_packet(self):
        udp_client = UDPClient('127.0.0.1', 6100)
        udp_client.set_udp_max_bytes(10)
        perf_pack = PerfCounterPack()
        perf_pack.put("abd", 123)
        perf_pack.obj_name = "testObj"
        perf_pack.time = int(time.time())
        perf_pack.time_type = "REALTIME"
        out = DataOutputX()
        out.write_pack(perf_pack)
        udp_client.write_buffer(out.get_bytes())

    def test_send_list(self):
        udp_client = UDPClient('127.0.0.1', 6100)
        pack_list = []

        perf_pack = PerfCounterPack()
        perf_pack.put("key1", 123)
        perf_pack.obj_name = "testObj"
        perf_pack.time = int(time.time())
        perf_pack.time_type = "REALTIME"
        out = DataOutputX()
        out.write_pack(perf_pack)
        pack_list.append(out.get_bytes())

        perf_pack = PerfCounterPack()
        perf_pack.put("key2", 456)
        perf_pack.obj_name = "testObj2"
        perf_pack.time = int(time.time())
        out = DataOutputX()
        out.write_pack(perf_pack)
        pack_list.append(out.get_bytes())

        udp_client.write_buffer_list(pack_list)

    def test_data_output(self):
        udp_client = UDPClient('127.0.0.1', 6100)
        out = DataOutputX(udp_client.conn)
        out.write_int32(123344)


if __name__ == "__main__":
    unittest.main()
