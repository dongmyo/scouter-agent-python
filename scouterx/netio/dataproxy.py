import time

from scouterx.common.netdata.alertpack import AlertPack
from scouterx.common.netdata.step_util import steps_to_bytes
from scouterx.common.netdata.textpack import TextPack
from scouterx.common.netdata.texttype.texttype import TextType
from scouterx.common.netdata.xlogprofilepack import XlogProfilePack
from scouterx.common.structure.lra.lra import Cache
from scouterx.common.util.hash_util import hash_string
from scouterx.conf.configure import Configure
from scouterx.netio.udpsender.udpsender import UDPSender

ac = Configure()

service_name_sent = Cache(10000)
obj_name_sent = Cache(100)
referer_sent = Cache(10000)
user_agent_sent = Cache(10000)
method_sent = Cache(10000)
apicall_sent = Cache(10000)
error_sent = Cache(10000)
login_sent = Cache(10000)
desc_sent = Cache(10000)
stack_element_sent = Cache(10000)
hash_message_sent = Cache(10000)


def reset_text_sent():
    service_name_sent.clear()
    obj_name_sent.clear()
    referer_sent.clear()
    user_agent_sent.clear()
    method_sent.clear()
    apicall_sent.clear()
    error_sent.clear()
    login_sent.clear()
    desc_sent.clear()
    stack_element_sent.clear()
    hash_message_sent.clear()


def send_service_name(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if service_name_sent.contains(hash):
        return hash
    service_name_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.SERVICE, hash, name))
    return hash


def send_hashed_message(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if hash_message_sent.contains(hash):
        return hash
    hash_message_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.HASH_MSG, hash, name))
    return hash


def send_obj_name(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if obj_name_sent.contains(hash):
        return hash
    obj_name_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.OBJECT, hash, name))
    return hash


def send_referer(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if referer_sent.contains(hash):
        return hash
    referer_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.REFERER, hash, name))
    return hash


def send_user_agent(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if user_agent_sent.contains(hash):
        return hash
    user_agent_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.USER_AGENT, hash, name))
    return hash


def send_method(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if method_sent.contains(hash):
        return hash
    method_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.METHOD, hash, name))
    return hash


def send_apicall(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if apicall_sent.contains(hash):
        return hash
    apicall_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.APICALL, hash, name))
    return hash


def send_error(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if error_sent.contains(hash):
        return hash
    error_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.ERROR, hash, name))
    return hash


def send_alert(level, title, message):
    if title == "":
        return
    pack = AlertPack()
    pack.obj_type = ac.obj_type
    pack.obj_hash = ac.obj_hash
    pack.level = level
    pack.title = title
    pack.message = message

    send_pack_direct(pack)


def send_login(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if login_sent.contains(hash):
        return hash
    login_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.LOGIN, hash, name))
    return hash


def send_desc(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if desc_sent.contains(hash):
        return hash
    desc_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.DESC, hash, name))
    return hash


def send_stack_element(name):
    if name == "":
        return 0
    hash = hash_string(name)
    if stack_element_sent.contains(hash):
        return hash
    stack_element_sent.add_key(hash)
    UDPSender().add_pack(TextPack(TextType.STACK_ELEMENT, hash, name))
    return hash


def send_xlog(pack):
    pack.obj_hash = ac.obj_hash
    UDPSender().send_pack_direct(pack)


def send_profile(steps, tctx):
    if not steps:
        return
    bulk_size = ac.profile_step_max_count
    count = len(steps) // bulk_size
    if count == 0:
        send_profile0(steps, tctx)
        return
    remainder = len(steps) % bulk_size
    for i in range(count):
        send_profile0(steps[i * bulk_size: (i + 1) * bulk_size], tctx)
    if remainder > 0:
        send_profile0(steps[count * bulk_size:], tctx)


def send_profile0(steps, tctx):
    if not steps:
        return

    pack = XlogProfilePack()
    pack.txid = tctx.txid
    pack.obj_hash = ac.obj_hash
    pack.profile = steps_to_bytes(steps)
    pack.service = tctx.service_hash
    pack.elapsed = int((time.time() - tctx.start_time) * 1000)
    tctx.profile_count += len(steps)
    tctx.profile_size += len(pack.profile)

    send_pack_direct(pack)


def send_pack_direct(pack):
    UDPSender().send_pack_direct(pack)
