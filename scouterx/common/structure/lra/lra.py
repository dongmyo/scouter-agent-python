from collections import OrderedDict
from threading import RLock


class Cache:
    def __init__(self, max_entries, on_evicted=None):
        self.max_entries = max_entries
        self.on_evicted = on_evicted
        self.cache = OrderedDict()
        self.lock = RLock()

    def add_key(self, key):
        self.add(key, None)

    def add(self, key, value):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                self.cache[key] = value
            else:
                if self.max_entries != 0 and len(self.cache) >= self.max_entries:
                    self.remove_oldest()
                self.cache[key] = value

    def get(self, key):
        with self.lock:
            value = self.cache.get(key)
            if value is not None:
                self.cache.move_to_end(key)
            return value

    def contains(self, key):
        with self.lock:
            return key in self.cache

    def empty(self):
        with self.lock:
            return len(self.cache) == 0

    def remove(self, key):
        with self.lock:
            if key in self.cache:
                value = self.cache.pop(key)
                if self.on_evicted:
                    self.on_evicted(key, value)

    def remove_oldest(self):
        with self.lock:
            key, value = self.cache.popitem(last=False)
            if self.on_evicted:
                self.on_evicted(key, value)

    def size(self):
        with self.lock:
            return len(self.cache)

    def clear(self):
        with self.lock:
            if self.on_evicted:
                for key, value in self.cache.items():
                    self.on_evicted(key, value)
            self.cache.clear()

    def get_values(self):
        with self.lock:
            return list(self.cache.values())


if __name__ == "__main__":
    def on_evicted(key, value):
        print(f"Evicted: {key} -> {value}")

    cache = Cache(max_entries=5, on_evicted=on_evicted)
    for i in range(6):
        cache.add(i, f"value_{i}")
    print("Cache Contents:", cache.get_values())
    cache.remove(2)
    print("Cache Contents after removing key 2:", cache.get_values())
    cache.add(6, "value_6")
    print("Cache Contents after adding key 6:", cache.get_values())
