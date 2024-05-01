import numpy

from scouterx.common.logger.logger import trace_logger
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.util.hexa_util import int_to_xlog_string32
from scouterx.common.util.time_util import millis_to_now
from scouterx.conf.configure import Configure
from scouterx.conf.exthandler import load_config_text, save_config_text
from scouterx.dump.dump import *
from scouterx.netio.dataproxy import reset_text_sent
from scouterx.strace.tctxmanager.tctxmanager import get_trace_context_by_txid, get_all_tctx

OBJECT_RESET_CACHE = "OBJECT_RESET_CACHE"
TRIGGER_THREAD_DUMP = "TRIGGER_THREAD_DUMP"
OBJECT_DUMP_FILE_LIST = "OBJECT_DUMP_FILE_LIST"
OBJECT_DUMP_FILE_DETAIL = "OBJECT_DUMP_FILE_DETAIL"
TRIGGER_BLOCK_PROFILE = "TRIGGER_BLOCK_PROFILE"
TRIGGER_MUTEX_PROFILE = "TRIGGER_MUTEX_PROFILE"
OBJECT_LIST_HEAP_DUMP = "OBJECT_LIST_HEAP_DUMP"
OBJECT_DOWNLOAD_HEAP_DUMP = "OBJECT_DOWNLOAD_HEAP_DUMP"
OBJECT_DELETE_HEAP_DUMP = "OBJECT_DELETE_HEAP_DUMP"
OBJECT_CALL_CPU_PROFILE = "OBJECT_CALL_CPU_PROFILE"
OBJECT_CALL_BLOCK_PROFILE = "OBJECT_CALL_BLOCK_PROFILE"
OBJECT_CALL_MUTEX_PROFILE = "OBJECT_CALL_MUTEX_PROFILE"
GET_CONFIGURE_WAS = "GET_CONFIGURE_WAS"
SET_CONFIGURE_WAS = "SET_CONFIGURE_WAS"
LIST_CONFIGURE_WAS = "LIST_CONFIGURE_WAS"
CONFIGURE_VALUE_TYPE = "CONFIGURE_VALUE_TYPE"
CONFIGURE_DESC = "CONFIGURE_DESC"
OBJECT_ACTIVE_SERVICE_LIST = "OBJECT_ACTIVE_SERVICE_LIST"
OBJECT_THREAD_DETAIL = "OBJECT_THREAD_DETAIL"


def handle(cmd, pack, in_data, out_data):
    ac = Configure()

    if cmd == "KEEP_ALIVE":
        if ac.is_trace():
            trace_logger.debug("KEEP_ALIVE")
        return None
    elif cmd == OBJECT_RESET_CACHE:
        if ac.is_trace():
            trace_logger.debug("OBJECT_RESET_CACHE")
        return reset_cache(pack)
    elif cmd == TRIGGER_THREAD_DUMP:
        if ac.is_trace():
            trace_logger.debug("TRIGGER_THREAD_DUMP")
        return heavy_all_stack_trace()
    elif cmd == OBJECT_DUMP_FILE_LIST:
        if ac.is_trace():
            trace_logger.debug("OBJECT_DUMP_FILE_LIST")
        return list_dump_files()
    elif cmd == OBJECT_DUMP_FILE_DETAIL:
        if ac.is_trace():
            trace_logger.debug("OBJECT_DUMP_FILE_DETAIL")
        stream_dump_file_contents(pack, out_data)
        return None
    elif cmd == TRIGGER_BLOCK_PROFILE:
        if ac.is_trace():
            trace_logger.debug("TRIGGER_BLOCK_PROFILE")
        trigger_block_profile(pack, out_data)
        return None
    elif cmd == TRIGGER_MUTEX_PROFILE:
        if ac.is_trace():
            trace_logger.debug("TRIGGER_MUTEX_PROFILE")
        trigger_mutex_profile(pack, out_data)
        return None
    elif cmd == OBJECT_LIST_HEAP_DUMP:
        if ac.is_trace():
            trace_logger.debug("OBJECT_LIST_HEAP_DUMP")
        return list_binary_dump(pack, out_data)
    elif cmd == OBJECT_DOWNLOAD_HEAP_DUMP:
        if ac.is_trace():
            trace_logger.debug("OBJECT_DOWNLOAD_HEAP_DUMP")
        return download_binary_dump(pack, out_data)
    elif cmd == OBJECT_DELETE_HEAP_DUMP:
        if ac.is_trace():
            trace_logger.debug("OBJECT_DELETE_HEAP_DUMP")
        return delete_binary_dump(pack, out_data)
    elif cmd == OBJECT_CALL_CPU_PROFILE:
        if ac.is_trace():
            trace_logger.debug("OBJECT_CALL_CPU_PROFILE")
        return trigger_binary_cpu_profile(pack, out_data)
    elif cmd == OBJECT_CALL_BLOCK_PROFILE:
        if ac.is_trace():
            trace_logger.debug("OBJECT_CALL_BLOCK_PROFILE")
        return trigger_binary_block_profile(pack, out_data)
    elif cmd == OBJECT_CALL_MUTEX_PROFILE:
        if ac.is_trace():
            trace_logger.debug("OBJECT_CALL_MUTEX_PROFILE")
        return trigger_binary_mutex_profile(pack, out_data)
    elif cmd == GET_CONFIGURE_WAS:
        if ac.is_trace():
            trace_logger.debug("GET_CONFIGURE_WAS")
        return load_config()
    elif cmd == SET_CONFIGURE_WAS:
        if ac.is_trace():
            trace_logger.debug("SET_CONFIGURE_WAS")
        return save_config(pack)
    elif cmd == LIST_CONFIGURE_WAS:
        if ac.is_trace():
            trace_logger.debug("LIST_CONFIGURE_WAS")
        return list_config()
    elif cmd == CONFIGURE_VALUE_TYPE:
        if ac.is_trace():
            trace_logger.debug("CONFIGURE_VALUE_TYPE")
        return list_config_value_type()
    elif cmd == CONFIGURE_DESC:
        if ac.is_trace():
            trace_logger.debug("CONFIGURE_DESC")
        return list_config_description()
    elif cmd == OBJECT_ACTIVE_SERVICE_LIST:
        if ac.is_trace():
            trace_logger.debug("OBJECT_ACTIVE_SERVICE_LIST")
        return get_active_list()
    elif cmd == OBJECT_THREAD_DETAIL:
        if ac.is_trace():
            trace_logger.debug("OBJECT_THREAD_DETAIL")
        return get_thread_detail(pack)
    else:
        if ac.is_trace():
            trace_logger.debug(f"UNKNOWN-HANDLER: {cmd}")


def delete_binary_dump(pack, out):
    if isinstance(pack, MapPack):
        file_name = pack.get_string("delfileName")
        return delete_binary_dump_files(file_name)
    return None


def download_binary_dump(pack, out):
    if isinstance(pack, MapPack):
        file_name = pack.get_string("fileName")
        download_binary_dump_files(out, file_name)


def list_binary_dump(pack, out):
    return list_binary_dump_files()


def trigger_binary_cpu_profile(pack, out):
    profile_binary_cpu(30)
    p = MapPack()
    p.put("success", BooleanValue(True))
    p.put("msg", "Success. It takes about 30 seconds.")
    return p


def trigger_block_profile(pack, out):
    profile_block(30, 1000 * 1000, 1)
    p = MapPack()
    p.put("success", BooleanValue(True))
    p.put("msg", "Success. It takes about 30 seconds.")
    return p


def trigger_mutex_profile(pack, out):
    profile_mutex(30, 10, 1)
    p = MapPack()
    p.put("success", BooleanValue(True))
    p.put("msg", "Success. It takes about 30 seconds.")
    return p


def trigger_binary_block_profile(pack, out):
    profile_block_binary_dump(30, 1000 * 1000)
    p = MapPack()
    p.put("success", BooleanValue(True))
    p.put("msg", "Success. It takes about 30 seconds.")
    return p


def trigger_binary_mutex_profile(pack, out):
    profile_mutex_binary_dump(30, 5)
    p = MapPack()
    p.put("success", BooleanValue(True))
    p.put("msg", "Success. It takes about 30 seconds.")
    return p


def get_thread_detail(param):
    p = MapPack()
    p.put("Thread Name", "[No Thread] End")
    p.put("State", "end")

    if not isinstance(param, MapPack):
        p.put("Stack Trace", "[info] scouter request param error.")
        return p

    txid = param.get_int64("txid")
    tctx = get_trace_context_by_txid(txid)
    if tctx is None:
        p.put("Stack Trace", f"[info] no traceContext. txid: {int_to_xlog_string32(txid)}")
        return p

    goid = tctx.goid
    p.put("Service Txid", int_to_xlog_string32(tctx.txid))
    p.put("Service Name", tctx.service_name)
    p.put("Service Elapsed", millis_to_now(tctx.start_time))
    p.put("Thread Id", -1)
    p.put("State", "n/a")
    p.put("Thread Name", f"[thread] {str(goid)}")
    p.put("Stack Trace", "stacktrace for thread is not yet supported")
    p.put("Last trace method", tctx.last_method)

    return p


def get_active_list():
    mpack = MapPack()

    id = mpack.new_list("id")
    elapsed = mpack.new_list("elapsed")
    service = mpack.new_list("service")
    name = mpack.new_list("name")
    txid = mpack.new_list("txid")
    ip = mpack.new_list("ip")
    state = mpack.new_list("stat")
    cpu = mpack.new_list("cpu")
    sql = mpack.new_list("sql")
    subcall = mpack.new_list("subcall")

    if_tctx = get_all_tctx()

    for tctx in if_tctx:
        if tctx is None:
            return mpack
        goid = tctx.goid
        id.add_int64(goid)
        elapsed.add_int32(millis_to_now(tctx.start_time))
        service.add_string(tctx.service_name)
        name.add_string(f"[thread] {goid}")
        txid.add_string(int_to_xlog_string32(tctx.txid))
        ip.add_string(tctx.remote_ip)
        state.add_string("n/a")
        cpu.add_int64(-1)
        sql.add_string("n/a")
        subcall.add_string("n/a")

    mpack.put("complete", BooleanValue(True))

    return mpack


def load_config():
    config_text = load_config_text()

    mp = MapPack()
    mp.put("agentConfig", config_text)

    desc_map = Configure.get_configure_desc_map()
    key_list = mp.new_list("configKey")
    for key, desc in desc_map.items():
        key_list.add_string(key)
    return mp


def save_config(pack):
    result = MapPack()
    result.put("result", False)

    if isinstance(pack, MapPack):
        text = pack.get_string("setConfig")
        success = save_config_text(text)
        if success:
            Configure().refresh()
            result.put("result", True)
    return result


def reset_cache(pack):
    reset_text_sent()
    return pack


def list_config():
    mp = MapPack()
    key_list = mp.new_list("key")
    value_list = mp.new_list("value")
    defaults_list = mp.new_list("default")

    desc_map = Configure().get_configure_desc_map()

    for key, desc in desc_map.items():
        key_list.add_string(desc.key)
        value_list.add_string(desc.value)
        defaults_list.add_string(desc.default_value)

    return mp


def list_config_description():
    mp = MapPack()
    desc_map = Configure.get_configure_desc_map()
    for key, desc in desc_map.items():
        mp.put(key, desc.desc)
    return mp


def list_config_value_type():
    mp = MapPack()
    desc_map = Configure.get_configure_desc_map()
    for key, desc in desc_map.items():
        mp.put(key, numpy.int32(desc.value_type))
    return mp
