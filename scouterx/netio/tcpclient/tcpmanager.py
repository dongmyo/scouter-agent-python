import time
from threading import Thread

from scouterx.common.logger.logger import error_logger
from scouterx.conf.configure import Configure
from scouterx.netio.tcpclient.tcpclient import get_tcp_client


def start_tcp():
    Configure()
    thread = Thread(target=_start_tcp)
    thread.start()


def _start_tcp():
    while True:
        min_sleep = 3000
        sleep = min_sleep
        max_sleep = 60000

        try:
            time.sleep(1.0)  # Sleep for 1 second
            client = get_tcp_client()
            if client.prepare():
                try:
                    client.process()
                except Exception as err:
                    error_logger.error(f"[scouter][err]connection to collector: {err}")
                    time.sleep(min(sleep, max_sleep) / 1000.0)  # Convert ms to seconds
                    sleep = min(sleep * 2, max_sleep)
            else:
                time.sleep(min(sleep, max_sleep) / 1000.0)
                sleep = min(sleep * 2, max_sleep)
        except Exception as e:
            error_logger.error(e)
