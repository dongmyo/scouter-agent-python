import threading

from scouterx.counter.metering import Metering


class ValueBucket:
    def __init__(self):
        self.value = 0.0
        self.count = 0


class ValueMetric:
    def __init__(self, sum=0.0, avg=0.0):
        self.sum = sum
        self.avg = avg


class ValueMetering:
    def __init__(self):
        self.metering = Metering(
            create=lambda: ValueBucket(),
            clear=lambda b: self.clear_bucket(b)
        )
        self.lock = threading.Lock()

    @classmethod
    def clear_bucket(cls, bucket):
        bucket.value = 0.0
        bucket.count = 0

    def add(self, value):
        with self.lock:
            bucket = self.metering.get_current_bucket()
            bucket.count += 1
            bucket.value += value

    def get_all_counter(self, period):
        sum = 0.0
        count = 0

        def handler(bucket):
            nonlocal sum, count
            sum += bucket.value
            count += bucket.count

        period = self.metering.search_on_handler(period, handler)
        avg = sum / count if count != 0 else 0.0
        return ValueMetric(sum=sum, avg=avg)
