import logging
import time
from threading import Thread, Event

from scouterx.common.netdata.objectpack import ObjectPack
from scouterx.common.util.hash_util import hash_string
from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_pack_direct
from scouterx.strace.tracemain import start_tracing_mode


def test_start_tracing_mode():
    ac = Configure()
    ac.set_trace(True)

    logging.error("error log test")
    logging.error("error log test %s", "(testing)")

    done_event = Event()

    obj_pack = ObjectPack()
    obj_pack.obj_name = "node-testcase-start"
    obj_pack.obj_hash = hash_string(obj_pack.obj_name)
    obj_pack.obj_type = "python"
    send_pack_direct(obj_pack)
    ac.obj_hash = obj_pack.obj_hash

    def send_periodically():
        while True:
            time.sleep(3)
            send_pack_direct(obj_pack)

    thread = Thread(target=send_periodically)
    thread.start()
    start_tracing_mode()

    done_event.wait()


if __name__ == "__main__":
    test_start_tracing_mode()
