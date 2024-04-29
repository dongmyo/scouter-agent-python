import threading
import time

from scouterx.common.logger.logger import info_logger
from scouterx.common.netdata.objectpack import ObjectPack
from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_obj_name, send_pack_direct


def start():
    t = threading.Thread(target=start_thread)
    t.start()


def start_thread():
    while True:
        time.sleep(2)
        send_obj_pack()


def send_obj_pack():
    ac = Configure()
    obj_name = ac.obj_name
    obj_hash = send_obj_name(obj_name)

    obj_pack = ObjectPack()
    obj_pack.obj_name = obj_name
    obj_pack.obj_hash = obj_hash
    obj_pack.obj_type = ac.obj_type
    obj_pack.version = '0.0.0'

    if ac.trace_obj_send:
        info_logger.info(f"[scouter] sendObjectPack: {obj_name}, {obj_hash}, {ac.obj_type}")

    send_pack_direct(obj_pack)

