import threading

from scouterx.counter.metering import Metering


class ServiceBucket:
    def __init__(self):
        self.count = 0
        self.elapsed = 0
        self.error = 0


class ServiceCounter:
    def __init__(self, tps=0.0, elapsed=0, error_rate=0.0):
        self.tps = tps
        self.elapsed = elapsed
        self.error_rate = error_rate


class ServiceMetering:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ServiceMetering, cls).__new__(cls)
                cls._instance.metering = Metering(
                    create=lambda: ServiceBucket(),
                    clear=lambda b: cls._instance.clear_bucket(b)
                )
        return cls._instance

    @staticmethod
    def clear_bucket(bucket):
        bucket.count = 0
        bucket.elapsed = 0
        bucket.error = 0

    def add(self, elapsed, err):
        with self._lock:
            if elapsed < 0:
                elapsed = 0
            bucket = self.metering.get_current_bucket()
            bucket.count += 1
            bucket.elapsed += elapsed
            if err:
                bucket.error += 1

    def get_all_counter(self, period):
        count_sum = 0
        elapsed_sum = 0
        error_sum = 0

        def handler(bucket):
            nonlocal count_sum, elapsed_sum, error_sum
            count_sum += bucket.count
            elapsed_sum += bucket.elapsed
            error_sum += bucket.error

        period = self.metering.search_on_handler(period, handler)

        tps = float(count_sum) / period if period != 0 else 0.0
        elapsed = elapsed_sum // count_sum if count_sum != 0 else 0
        error_rate = (float(error_sum) / count_sum * 100.0) if count_sum != 0 else 0.0

        return ServiceCounter(tps=tps, elapsed=elapsed, error_rate=error_rate)
