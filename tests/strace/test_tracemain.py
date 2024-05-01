import time
import unittest
from threading import Thread
from contextlib import contextmanager

from scouterx.common.netdata.objectpack import ObjectPack
from scouterx.common.util.hash_util import hash_string
from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_pack_direct
from scouterx.strace.tracemain import start_service, end_service, start_method, end_method


class TestXlog(unittest.TestCase):
    def test_xlog(self):
        register_obj()
        service = "/test-service/witprofile/0"
        with simulated_service(service, "10.10.10.10"):
            test_method1(None)
            test_method1(None)
            test_method1(None)
            test_method1(None)
            test_method1(None)
            time.sleep(0.200)

    def test_xlog_with_go(self):
        register_obj()
        service = "/test-service/withgo/0"
        with simulated_service(service, "10.10.10.10"):
            test_method1(None)

            thread_with_trace(None, "testMethod4Go()", test_method4go)
            time.sleep(0.030)

            test_method1(None)
            time.sleep(0.200)


def register_obj():
    obj_pack = ObjectPack()
    obj_pack.obj_name = "node-testcase0"
    obj_pack.obj_hash = hash_string(obj_pack.obj_name)
    obj_pack.obj_type = "golang"
    send_pack_direct(obj_pack)
    ac = Configure()
    ac.obj_hash = obj_pack.obj_hash
    return obj_pack


def thread_with_trace(ctx, service_name, func):
    t = Thread(target=func, args=(ctx,))
    t.start()
    t.join()


@contextmanager
def simulated_service(service, remote_ip):
    ctx = start_service(None, service, remote_ip)
    try:
        yield ctx
    finally:
        end_service(ctx)


def test_method1(ctx=None):
    method_step = start_method(ctx)
    time.sleep(0.150)  # Simulating workload
    end_method(ctx, method_step)


def test_method4go(ctx=None):
    method_step = start_method(ctx)
    time.sleep(0.050)  # Simulating workload
    end_method(ctx, method_step)


if __name__ == '__main__':
    unittest.main()
