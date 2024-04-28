from collections import OrderedDict
from threading import Lock


class CacheSet:
    def __init__(self, max_size):
        self.table = OrderedDict()
        self.maxSize = max_size
        self.lock = Lock()

    def add(self, item):
        with self.lock:
            if item not in self.table:
                self._remove_exceeded()
                self.table[item] = None

    def _remove_exceeded(self):
        removal_count = len(self.table) - self.maxSize
        if removal_count < 0:
            return

        removals = []
        for _ in range(removal_count + 1):
            item = next(iter(self.table))
            removals.append(item)

        for item in removals:
            self.table.pop(item)

    def contains(self, item):
        with self.lock:
            return item in self.table

    def empty(self):
        with self.lock:
            return not self.table

    def size(self):
        with self.lock:
            return len(self.table)

    def clear(self):
        with self.lock:
            self.table.clear()

    def __str__(self):
        return f"CacheSet[{self.size()}]"


if __name__ == "__main__":
    cache = CacheSet(10)
    for i in range(15):
        cache.add(i)
    print(str(cache))
    print("Contains 0:", cache.contains(0))
    print("Contains 15:", cache.contains(15))
    cache.clear()
    print("Empty after clear:", cache.empty())
