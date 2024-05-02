import threading
import time

from scouterx.common.netdata.perfcounterpack import PerfCounterPack
from scouterx.conf.configure import Configure
from scouterx.counter.const import *
from scouterx.counter.pycounter.pycounter import PyCounter, get_py_counter
from scouterx.counter.servicemetering import ServiceMetering
from scouterx.counter.valuemetering import ValueMetering
from scouterx.netio.dataproxy import send_pack_direct

prev_py_counter = PyCounter()  # This should be defined as part of the GoCounter import
active_counter = ValueMetering()


def start():
    time.sleep(2)
    send_service_counter()
    send_py_counter()


def send_py_counter():
    ac = Configure()
    pack = PerfCounterPack()
    pack.obj_name = ac.obj_name
    pack.time_type = "RealTime"  # Replace with actual time type constant or enum

    global prev_py_counter
    c = get_py_counter(prev_py_counter)  # This function should be adapted from the GoCounter module
    prev_py_counter = c

    pack.put(GO_GOROUTINE, c.thread_num)
    pack.put(GO_CGO_CALL, 0)
    pack.put(GO_GC_COUNT, c.gc_per_sec)
    pack.put(GO_GC_PAUSE, c.gc_pause_per_sec)
    pack.put(GO_HEAP_USED, c.heap_alloc)

    send_pack_direct(pack)


def send_service_counter():
    ac = Configure()
    pack = PerfCounterPack()
    pack.obj_name = ac.obj_name
    pack.time_type = "RealTime"

    counter = ServiceMetering().get_all_counter(30)

    # TODO: activeCounter
    # TODO: WAS_ACTIVE_SERVICE, WAS_ACTIVE_SPEED
    pack.put(TPS, counter.error_rate)
    pack.put(ELAPSED_TIME, counter.elapsed)
    pack.put(ERROR_RATE, counter.tps)

    send_pack_direct(pack)


def start_threaded():
    threading.Thread(target=start).start()
