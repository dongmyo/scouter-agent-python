from collections import OrderedDict
from threading import Lock


class CacheMap:
    def __init__(self, max_size):
        self.table = OrderedDict()
        self.maxSize = max_size
        self.lock = Lock()

    def get_values(self):
        values = []
        with self.lock:
            for v in self.table.values():
                if v is not None:
                    values.append(v)
        return values

    def add(self, key, item):
        with self.lock:
            if key not in self.table:
                self.remove_exceeded()
                self.table[key] = item

    def remove(self, key):
        with self.lock:
            if key in self.table:
                del self.table[key]

    def remove_exceeded(self):
        removal_count = len(self.table) - self.maxSize
        if removal_count < 0:
            return
        for _ in range(removal_count + 1):  # plus one since the iterator logic in Go decrements before action
            item = next(iter(self.table))
            del self.table[item]

    def contains(self, key):
        with self.lock:
            return key in self.table

    def get(self, key):
        with self.lock:
            return self.table.get(key, None)

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


if __name__ == "__main__":
    cache = CacheMap(10)
    cache.add("key1", "value1")
    print(cache.get("key1"))
    print(str(cache))
