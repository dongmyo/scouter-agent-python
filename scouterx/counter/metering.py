import threading
import time


def get_timestamp():
    return int(time.time())


class Metering:
    def __init__(self, create, clear):
        self.bucket_size = 301
        self.current_time = get_timestamp()
        self.pos = self.current_time % self.bucket_size
        self.table = [create() for _ in range(self.bucket_size)]
        self.clear = clear
        self.lock = threading.Lock()

    def get_current_bucket(self):
        pos = self.get_position()
        return self.table[pos]

    def get_position(self):
        with self.lock:
            cur_time = get_timestamp()
            if cur_time != self.current_time:
                for i in range(min(cur_time - self.current_time, self.bucket_size)):
                    self.pos = (self.pos + 1) % self.bucket_size
                    self.clear(self.table[self.pos])
                self.current_time = cur_time
                self.pos = cur_time % self.bucket_size
            return self.pos

    def check(self, period):
        if period >= self.bucket_size:
            period = self.bucket_size - 1
        return period

    def step_back(self, pos):
        return (pos - 1) % self.bucket_size

    def search_on_handler(self, period, handler):
        period = self.check(period)
        pos = self.get_position()
        for i in range(period):
            handler(self.table[pos])
            pos = self.step_back(pos)
        return period

    def search(self, period):
        period = self.check(period)
        pos = self.get_position()
        out = []
        for i in range(period):
            out.append(self.table[pos])
            pos = self.step_back(pos)
        return out
