import hashlib
import os
import socket
import threading
import time
from datetime import datetime
from collections import OrderedDict
from configparser import ConfigParser

from scouterx.common.util.os_util import get_scouter_path
from scouterx.conf.opserver import obj_change_notify


class ValueType:
    VT_VALUE = 1
    VT_NUM = 2
    VT_BOOL = 3
    VT_COMMA_SEPARATED_VALUE = 4
    VT_COMMA_COLON_SEPARATED_VALUE = 5


desc_map = OrderedDict()


class ConfigureDesc:
    def __init__(self, key, value, default_value, desc, value_type):
        self.key = key
        self.value = value
        self.default_value = default_value
        self.desc = desc
        self.value_type = value_type


class Configure:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(Configure, cls).__new__(cls)
                cls._instance.init()
                threading.Thread(target=cls._instance.run).start()
            return cls._instance

    def __init__(self):
        self.lock = threading.Lock()
        self.last_modified = datetime.min
        self._trace = False
        self.trace_obj_send = False
        self.send_queue_size = 3000
        self.obj_hash = 0
        self.obj_name = ""
        self.obj_type = ""
        self.obj_name_simple = ""
        self.net_collector_ip = "127.0.0.1"
        self.net_collector_udp_port = 6100
        self.net_collector_tcp_port = 6100
        self.net_collector_tcp_so_timeout_ms = 60000
        self.net_collector_tcp_connection_timeout_ms = 3000
        self.udp_max_bytes = 60000
        self.stuck_service_base_time_ms = 300000
        self.stuck_service_remove_enabled = True
        self.stuck_service_alert_enabled = True
        self.trace_activeservice_yellow_time = 3000
        self.trace_activeservice_red_time = 8000
        self.profile_step_max_keep_in_memory_count = 2048
        self.profile_step_max_count = 1024
        self.profile_http_querystring_enabled = False
        self.profile_http_header_enabled = False
        self.profile_http_header_keys = ""
        self.trace_http_client_ip_header_key = ""
        self.xlog_discard_service_patterns = ""
        self.xlog_discard_service_show_error = True
        self.xlog_sampling_exclude_patterns = ""
        self.xlog_sampling_enabled = False
        self.xlog_sampling_only_profile = False
        self.xlog_sampling_step1_ms = 100
        self.xlog_sampling_step1_rate_pct = 2
        self.xlog_sampling_step2_ms = 500
        self.xlog_sampling_step2_rate_pct = 7
        self.xlog_sampling_step3_ms = 1000
        self.xlog_sampling_step3_rate_pct = 15
        self.xlog_sampling_over_rate_pct = 3000
        self.xlog_patterned_sampling_enabled = False
        self.xlog_patterned_sampling_service_patterns = ""
        self.xlog_patterned_sampling_only_profile = False
        self.xlog_patterned_sampling_step1_ms = 100
        self.xlog_patterned_sampling_step1_rate_pct = 2
        self.xlog_patterned_sampling_step2_ms = 500
        self.xlog_patterned_sampling_step2_rate_pct = 7
        self.xlog_patterned_sampling_step3_ms = 1000
        self.xlog_patterned_sampling_step3_rate_pct = 15
        self.xlog_patterned_sampling_over_rate_pct = 3000
        self.xlog_patterned2_sampling_enabled = False
        self.xlog_patterned2_sampling_service_patterns = ""
        self.xlog_patterned2_sampling_only_profile = False
        self.xlog_patterned2_sampling_step1_ms = 100
        self.xlog_patterned2_sampling_step1_rate_pct = 2
        self.xlog_patterned2_sampling_step2_ms = 500
        self.xlog_patterned2_sampling_step2_rate_pct = 7
        self.xlog_patterned2_sampling_step3_ms = 1000
        self.xlog_patterned2_sampling_step3_rate_pct = 15
        self.xlog_patterned2_sampling_over_rate_pct = 3000
        self.xlog_patterned3_sampling_enabled = False
        self.xlog_patterned3_sampling_service_patterns = ""
        self.xlog_patterned3_sampling_only_profile = False
        self.xlog_patterned3_sampling_step1_ms = 100
        self.xlog_patterned3_sampling_step1_rate_pct = 2
        self.xlog_patterned3_sampling_step2_ms = 500
        self.xlog_patterned3_sampling_step2_rate_pct = 7
        self.xlog_patterned3_sampling_step3_ms = 1000
        self.xlog_patterned3_sampling_step3_rate_pct = 15
        self.xlog_patterned3_sampling_over_rate_pct = 3000

    def init(self):
        # TODO read system prop
        self.refresh()

    def run(self):
        while True:
            time.sleep(5)
            self.refresh()

    def refresh(self):
        with self.lock:
            file_path = self.get_conf_file_path()
            try:
                info = os.stat(file_path)
                if info.st_mtime > self.last_modified.timestamp():
                    self.load_properties(file_path)
                    self.last_modified = datetime.fromtimestamp(info.st_mtime)
            except FileNotFoundError:
                pass
            except Exception as e:
                # TODO logging
                pass

    @classmethod
    def get_conf_file_path(cls):
        scouter_conf_file = os.getenv("SCOUTER_CONFIG", os.getenv("scouter.config"))
        if not scouter_conf_file:
            path = get_scouter_path()
            os.makedirs(os.path.join(path, "conf"), exist_ok=True)
            scouter_conf_file = os.path.join(path, "conf", "scouter.conf")
        return scouter_conf_file

    def set_trace(self, mode):
        self._trace = mode

    def is_trace(self):
        return self._trace

    def reset_obj_name_and_type(self, props):
        default_name = "py1"
        hostname = socket.gethostname()
        if not hostname:
            hostname = "unknown"

        old_obj_name = self.obj_name
        new_obj_simple_name = self.string_of(props, "obj_name", default_name, "object name")
        obj_host_name = self.string_of(props, "obj_host_name", hostname, "object host name")
        self.obj_name_simple = new_obj_simple_name
        self.obj_name = f"/{obj_host_name}/{new_obj_simple_name}"
        self.obj_hash = self.hash_string(self.obj_name)

        self.obj_type = self.string_of(props, "obj_type", "golang", "object type (monitoring group)")
        if old_obj_name != self.obj_name:
            obj_change_notify()

    def string_of(self, props, key, default_value, desc):
        value = props.get(key, default_value)
        self.update_description(key, value, default_value, desc, ValueType.VT_VALUE)
        return value

    @classmethod
    def update_description(cls, key, value, default_value, desc, value_type):
        desc_map[key] = ConfigureDesc(key, value, default_value, desc, value_type)

    @classmethod
    def hash_string(cls, input_string):
        return int(hashlib.md5(input_string.encode()).hexdigest(), 16)

    def load_properties(self, file_path):
        config = ConfigParser()
        config.read(file_path)
        for section in config.sections():
            for key, value in config.items(section):
                setattr(self, key, value)


if __name__ == '__main__':
    config = Configure()
    config.set_trace(True)
    print(config.is_trace())