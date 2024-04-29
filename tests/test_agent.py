import random
import time
from threading import Thread, Lock, Event

from scouterx.agent import ScouterAgent
from scouterx.strace.tracemain import start_service, end_service, start_method, end_method
from tests.strace.test_tracemain import thread_with_trace


def test_scouter_agent():
    done_event = Event()

    ScouterAgent.initialize()
    for _ in range(5):
        Thread(target=load_test).start()

    Thread(target=mutex_lock).start()

    done_event.wait()


def load_test():
    while True:
        random_sleeps()


def mutex_lock():
    # Configure the mutex profile logging level, if applicable in Python
    mu = Lock()
    for i in range(10):
        Thread(target=lambda: lock_cycle(mu)).start()


def lock_cycle(mu):
    while True:
        with mu:
            time.sleep(0.1)  # Lock held for 100 milliseconds


def random_sleeps():
    ctx = start_service("randomSleeps")
    try:
        random_sleep(ctx, 1500)
        thread_with_trace(ctx, "myPyFunc()", lambda cascade_go_ctx: random_sleep(cascade_go_ctx, 500))
        random_sleep(ctx, 800)
    finally:
        end_service(ctx)


def random_sleep(ctx, ms):
    step = start_method(ctx)
    try:
        ms_random = random.randint(0, ms)
        sleep_func(ctx, ms_random)
    finally:
        end_method(ctx, step)


def sleep_func(ctx, ms):
    step = start_method(ctx)
    try:
        time.sleep(ms / 1000.0)  # Python's sleep takes seconds
    finally:
        end_method(ctx, step)


if __name__ == "__main__":
    test_scouter_agent()
