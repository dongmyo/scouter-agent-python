from threading import Lock

from scouterx.conf.configure import Configure
from scouterx.conf.opserver import add_obj_changed_observer
from scouterx.netio.dataproxy import send_obj_name
from scouterx.strace.tracemain import start_tracing_mode
from scouterx.task.agenttask import agenttask
from scouterx.task.countertask import countertask


class ObjNameChangeObserver:
    def run(self):
        ac = Configure()
        send_obj_name(ac.obj_name)


class ScouterAgent:
    _instance_lock = Lock()
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            with cls._instance_lock:
                if not cls._initialized:
                    cls._initialize()
                    cls._initialized = True

    @classmethod
    def _initialize(cls):
        Configure()
        start_tracing_mode()
        agenttask.send_obj_pack()
        agenttask.start()
        add_obj_changed_observer(ObjNameChangeObserver())
        countertask.start()
