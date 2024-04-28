import random
import threading
import time


class KeyGen:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._random = random.Random()
        self._random.seed(time.time())

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def next(self):
        with self._lock:
            return self._random.getrandbits(63)  # Generates a 63-bit integer


if __name__ == "__main__":
    key_gen_instance = KeyGen.get_instance()
    print(key_gen_instance.next())
