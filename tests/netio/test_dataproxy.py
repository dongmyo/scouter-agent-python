import os
import time
import unittest

from scouterx.common.netdata.messagestep import MessageStep
from scouterx.common.netdata.objectpack import ObjectPack, ObjectPack2
from scouterx.common.netdata.xlogpack import XlogPack
from scouterx.common.util.hash_util import hash_string
from scouterx.common.util.ip_util import ip_to_bytes
from scouterx.common.util.keygen.keygen import KeyGen
from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_service_name, send_xlog, send_pack_direct
from scouterx.netio.tracecontext import TraceContext
from scouterx.netio.udpsender.udpsender import UDPSender


class TestSendXlog(unittest.TestCase):
    def test_send_xlog(self):
        service = "/test-service/0"
        self.register_obj()
        xlog = XlogPack()
        xlog.txid = KeyGen.get_instance().next()
        xlog.x_type = "XTYPE_WEB_SERVICE"
        xlog.service = send_service_name(service)
        xlog.elapsed = 100
        xlog.discard_type = "XLOG_DISCARD_NONE"
        xlog.ipaddr = ip_to_bytes("127.0.0.1")
        send_xlog(xlog)

    def register_obj(self):
        obj_pack = ObjectPack()
        obj_pack.obj_name = "node-testcase0"
        obj_pack.obj_hash = hash_string(obj_pack.obj_name)
        obj_pack.obj_type = "golang"
        send_pack_direct(obj_pack)
        Configure().obj_hash = obj_pack.obj_hash
        return obj_pack

    def test_send_profile_and_xlog(self):
        self.register_obj()
        service = "/test-service/withprofile/0"
        service_hash = send_service_name(service)
        txid = KeyGen.get_instance().next()

        context = TraceContext()
        context.x_type = "XTYPE_WEB_SERVICE"
        context.txid = txid
        context.service_hash = service_hash

        push_step = MessageStep("test-push0", 0)
        context.profile.push(push_step)
        context.profile.add(MessageStep("test-message0", 0))
        context.profile.pop(push_step)
        context.profile.close(True)

        xlog = XlogPack()
        xlog.txid = context.txid
        xlog.x_type = context.x_type
        xlog.service = context.service_hash
        xlog.elapsed = 100
        xlog.discard_type = "XLOG_DISCARD_NONE"
        xlog.ipaddr = ip_to_bytes("127.0.0.1")
        send_xlog(xlog)

    def test_send_object_pack(self):
        os.environ["NET_COLLECTOR_IP"] = "127.0.0.1"
        os.environ["NET_COLLECTOR_UDP_PORT"] = "6002"
        os.environ["NET_COLLECTOR_TCP_PORT"] = "6002"
        os.environ["UDP_MAX_BYTES"] = "60000"

        sender = UDPSender()
        while True:
            for i in range(200):
                obj_pack = ObjectPack2()
                obj_pack.obj_name = f"node{i}"
                obj_pack.obj_hash = hash_string(obj_pack.obj_name)
                obj_pack.obj_type = "host"
                obj_pack.family = 2
                sender.add_pack(obj_pack)
                # time.sleep(3)
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
