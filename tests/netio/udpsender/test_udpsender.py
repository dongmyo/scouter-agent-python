import time
import unittest

from scouterx.common.constants.timeconstant.timeconstants import REALTIME
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.objectpack import ObjectPack
from scouterx.common.netdata.perfcounterpack import PerfCounterPack
from scouterx.common.util.hash_util import hash_string
from scouterx.netio.udpsender.udpsender import UDPSender


class TestUDPSender(unittest.TestCase):

    def test_send_perf_pack(self):
        sender = UDPSender()
        perf_pack = PerfCounterPack()
        perf_pack.put("abc", 123)
        perf_pack.obj_name = "testObj"
        perf_pack.time = int(time.time())
        perf_pack.time_type = REALTIME
        out = DataOutputX()
        out.write_pack(perf_pack)
        buffer = out.get_bytes()
        sender.add_buffer(buffer)
        print(f"queue size: {sender.get_queue_size()}")

        # Simulating a long running process to monitor behavior; use with caution
        time.sleep(1)  # reduced sleep for test practicality

    def test_send_object_pack1(self):
        sender = UDPSender()
        obj_pack = ObjectPack()
        obj_pack.obj_name = "node-test0"
        obj_pack.obj_hash = hash_string(obj_pack.obj_name)
        obj_pack.obj_type = "host"
        sender.add_pack(obj_pack)

    def test_send_object_pack(self):
        sender = UDPSender()
        while True:
            for i in range(200):
                obj_pack = ObjectPack()
                obj_pack.obj_name = f"node{i}"
                obj_pack.obj_hash = hash_string(obj_pack.obj_name)
                obj_pack.obj_type = "host"
                sender.add_pack(obj_pack)
            # Sleep to simulate some time for the sender to process
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
