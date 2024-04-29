import threading
import time

from scouterx.common.netdata.listvalue import ListValue
from scouterx.common.netdata.perfcounterpack import PerfCounterPack
from scouterx.conf.configure import Configure
from scouterx.counter.const import *
from scouterx.counter.pycounter.pycounter import PyCounter, get_py_counter
from scouterx.counter.servicemetering import ServiceMetering
from scouterx.counter.valuemetering import ValueMetering
from scouterx.netio.dataproxy import send_pack_direct
from scouterx.strace.tctxmanager.tctxmanager import get_active_count

prev_py_counter = PyCounter()
active_counter = ValueMetering()


def start():
    threading.Thread(target=start_real_time_counter).start()
    threading.Thread(target=start_5min_counter).start()


def start_real_time_counter():
    while True:
        time.sleep(2)
        pack = get_all_counter_on_pack()
        send_pack_direct(pack)


def start_5min_counter():
    while True:
        time.sleep(1)
        pack = get_all_5min_counter_on_pack()
        send_pack_direct(pack)


def get_all_counter_on_pack():
    ac = Configure()
    pack = PerfCounterPack()
    pack.obj_name = ac.obj_name
    pack.time_type = PerfCounterPack.TimeTypeRealTime

    global prev_py_counter
    c = get_py_counter(prev_py_counter)
    prev_py_counter = c

    pack.put(PY_THREAD, c.thread_num)
    pack.put(PY_GC_COUNT, c.gc_per_sec)
    pack.put(PY_GC_PAUSE, c.gc_pause_per_sec)
    pack.put(PY_HEAP_USED, c.heap_alloc)

    sc = ServiceMetering().get_all_counter(30)
    pack.put(TPS, sc.tps)
    pack.put(ELAPSED_TIME, sc.elapsed)
    pack.put(ERROR_RATE, sc.error_rate)

    active_counts = get_active_count()
    active_sum = active_counts[0] + active_counts[1] + active_counts[2]
    active_counter.add(active_sum)
    active = active_counter.get_all_counter(30).avg
    pack.put(ACTIVE_SERVICE, active)

    active_speed = ListValue()
    active_speed.add_int64(active_counts[0])
    active_speed.add_int64(active_counts[1])
    active_speed.add_int64(active_counts[2])

    pack.put(ACTIVE_SPEED, active_speed)

    return pack


def get_all_5min_counter_on_pack():
    ac = Configure()
    pack = PerfCounterPack()
    pack.obj_name = ac.obj_name
    pack.time_type = PerfCounterPack.TimeTypeFiveMin

    sc = ServiceMetering().get_all_counter(300)
    pack.put(TPS, sc.tps)
    pack.put(ELAPSED_TIME, sc.elapsed)
    pack.put(ERROR_RATE, sc.error_rate)

    active = active_counter.get_all_counter(300).avg
    pack.put(ACTIVE_SERVICE, active)

    return pack
