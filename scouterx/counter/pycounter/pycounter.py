import threading
import time
import psutil

stats_lock = threading.Lock()


class PyCounter:
    def __init__(self, timestamp=0, thread_num=0, heap_alloc=0, gc_per_sec=0.0, gc_pause_per_sec=0.0, m_pause_total_ns=0, m_num_gc=0):
        self.timestamp = timestamp
        self.thread_num = thread_num
        self.heap_alloc = heap_alloc
        self.gc_per_sec = gc_per_sec
        self.gc_pause_per_sec = gc_pause_per_sec
        self.m_pause_total_ns = m_pause_total_ns
        self.m_num_gc = m_num_gc


def get_py_counter(prev):
    with stats_lock:
        now_nano = int(time.time() * 1e9)
        process = psutil.Process()

        counter = PyCounter(timestamp=now_nano)
        counter.thread_num = threading.active_count()
        counter.heap_alloc = process.memory_info().rss  # Resident Set Size

        gc_pause_total_ns = 0  # Hypothetical: sum of GC pauses in nanoseconds
        gc_count = 0  # Hypothetical: count of GC events

        counter.m_pause_total_ns = gc_pause_total_ns
        counter.m_num_gc = gc_count

        if prev.timestamp != 0:
            duration = now_nano - prev.timestamp
            counter.gc_pause_per_sec = (gc_pause_total_ns - prev.m_pause_total_ns) / duration * 1000
            counter.gc_per_sec = (gc_count - prev.m_num_gc) / (duration / 1e9)

        return counter


if __name__ == '__main__':
    prev_counter = PyCounter()  # This would be stored from a previous call
    current_counter = get_py_counter(prev_counter)
