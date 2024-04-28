import queue
import threading


class ChannelFactory:
    _lock = threading.Lock()
    _udp_channel = None

    @classmethod
    def get_udp_channel(cls):
        with cls._lock:
            if cls._udp_channel is None:
                send_queue_size = cls.get_instance().send_queue_size
                cls._udp_channel = queue.Queue(maxsize=send_queue_size)
            return cls._udp_channel

    @staticmethod
    def get_instance():
        class Config:
            def __init__(self):
                self.send_queue_size = 100

        return Config()
