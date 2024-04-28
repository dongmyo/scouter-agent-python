import time
from collections import OrderedDict
from threading import Lock, Thread, Event


class CacheMap:
    def __init__(self, max_size):
        self.table = OrderedDict()
        self.maxSize = max_size
        self.lock = Lock()
        self.init_cleanup_task()

    def get_values(self):
        with self.lock:
            return list(self.table.values())

    def add(self, key, item):
        with self.lock:
            if key not in self.table:
                self._remove_exceeded()
                self.table[key] = item

    def remove(self, key):
        with self.lock:
            if key in self.table:
                del self.table[key]

    def _remove_exceeded(self):
        while len(self.table) >= self.maxSize:
            self.table.popitem(last=False)

    def contains(self, key):
        with self.lock:
            return key in self.table

    def get(self, key):
        with self.lock:
            return self.table.get(key)

    def empty(self):
        with self.lock:
            return len(self.table) == 0

    def size(self):
        with self.lock:
            return len(self.table)

    def clear(self):
        with self.lock:
            self.table.clear()

    def __str__(self):
        with self.lock:
            return f"CacheMap[{len(self.table)}]"

    def init_cleanup_task(self):
        def cleanup():
            while True:
                with self.lock:
                    if len(self.table) > self.maxSize / 2:
                        time.sleep(0.5)
                        # TODO
                    else:
                        time.sleep(0.1)
                        # TODO

        Thread(target=cleanup, daemon=True).start()


if __name__ == "__main__":
    cache = CacheMap(10)
    for i in range(15):
        cache.add(i, str(i))
    print(cache.get_values())
    print(str(cache))
