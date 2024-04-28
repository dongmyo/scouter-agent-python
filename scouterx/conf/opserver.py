from abc import ABC, abstractmethod
from threading import RLock
from typing import Dict

observer_lock = RLock()
observers: Dict[str, "Runnable"] = {}
obj_change_observer: "Runnable | None" = None


class Runnable(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses should implement this!")


def add_to_conf_observer(name, r):
    global observers
    with observer_lock:
        observers[name] = r


def add_obj_changed_observer(r):
    global obj_change_observer
    with observer_lock:
        obj_change_observer = r


def conf_change_notify():
    global observers
    with observer_lock:
        for r in observers.values():
            r.run()


def obj_change_notify():
    global obj_change_observer
    with observer_lock:
        if obj_change_observer is not None:
            obj_change_observer.run()
