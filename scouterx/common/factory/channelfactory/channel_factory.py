import queue
import threading

from scouterx.conf.configure import Configure


class ChannelFactory:
    _lock = threading.Lock()
    _udp_channel = None

    @classmethod
    def get_udp_channel(cls):
        with cls._lock:
            if cls._udp_channel is None:
                send_queue_size = Configure().send_queue_size
                cls._udp_channel = queue.Queue(maxsize=send_queue_size)
            return cls._udp_channel
