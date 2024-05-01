import os
import socket
import threading
import time
from collections import OrderedDict
from copy import deepcopy

import javaproperties
import numpy

import scouterx.common.logger.logger
from scouterx.common.util.hash_util import hash_string
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
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.initialized = False
            return cls._instance

    def __init__(self):
        if not self.initialized:
            scouterx.common.logger.logger.init()

            self.lock = threading.Lock()
            self.last_modified = 0
            self._trace = False
            self.initialize_properties()

            self.init()
            self.run_thread()

            self.initialized = True

    def initialize_properties(self):
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
        self.refresh()

    def run_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        while True:
            time.sleep(5)
            self.refresh()

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
        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = "unknown"
        old_obj_name = self.obj_name
        new_obj_simple_name = self.string_of(props, "obj_name", default_name, "object name")
        obj_host_name = self.string_of(props, "obj_host_name", hostname, "object host name")
        self.obj_name_simple = new_obj_simple_name
        self.obj_name = f"/{obj_host_name}/{new_obj_simple_name}"
        self.obj_hash = numpy.int32(hash_string(self.obj_name))
        self.obj_type = self.string_of(props, "obj_type", "golang", "object type (monitoring group)")
        if old_obj_name != self.obj_name:
            obj_change_notify()

    def refresh(self):
        with self.lock:
            file_path = self.get_conf_file_path()
            try:
                info = os.stat(file_path)
            except FileNotFoundError:
                return
            except Exception as e:
                # TODO: logging the exception
                print(f"Error loading config file {file_path}: {e}")
                return

            if info is None or info.st_mtime > (self.last_modified or 0):
                props = dict(os.environ)

                try:
                    with open(file_path, 'rb') as file:
                        file_props = javaproperties.load(file)

                        if file_props:
                            props.update(file_props)
                except Exception as e:
                    print(f"Error loading config file {file_path}: {e}")
                    return

                props = {k: v for k, v in props.items() if v}

                self.add_to_conf(props)

                if info:
                    self.last_modified = info.st_mtime

                obj_change_notify()

    def get_configure_desc_map(self):
        return deepcopy(desc_map)

    def bool_of(self, props, key, default_value, desc):
        value = props.get(key, str(default_value)).lower() in ['true', '1', 't', 'y', 'yes']
        desc_map[key] = ConfigureDesc(
            key=key,
            value=str(value),
            default_value=str(default_value),
            desc=desc,
            value_type=ValueType.VT_BOOL
        )
        return value

    def int_of(self, props, key, default_value, desc):
        try:
            value = int(props.get(key, default_value))
        except ValueError:
            value = default_value  # Default fallback if conversion fails
        desc_map[key] = ConfigureDesc(
            key=key,
            value=str(value),
            default_value=str(default_value),
            desc=desc,
            value_type=ValueType.VT_NUM
        )

        return value

    def string_of(self, props, key, default_value, desc):
        value = props.get(key, default_value)
        self.update_description(key, value, default_value, desc, ValueType.VT_VALUE)
        return value

    def string_of_type(self, props, key, default_value, value_type, desc):
        value = props.get(key, default_value)
        self.update_description(key, value, default_value, desc, value_type)
        return value

    def add_to_conf(self, props):
        self.reset_obj_name_and_type(props)

        self._trace = props.get('_trace', False)

        self.trace_obj_send = self.bool_of(props, 'trace_obj_send', False, '')
        self.send_queue_size = self.int_of(props, 'send_queue_size', 3000, '')

        self.net_collector_ip = self.string_of(props, 'net_collector_ip', '127.0.0.1', '')
        self.net_collector_udp_port = self.int_of(props, 'net_collector_udp_port', 6100, '')
        self.net_collector_tcp_port = self.int_of(props, 'net_collector_tcp_port', 6100, '')
        self.net_collector_tcp_so_timeout_ms = self.int_of(props, 'net_collector_tcp_so_timeout_ms', 60000, '')
        self.net_collector_tcp_connection_timeout_ms = self.int_of(props, 'net_collector_tcp_connection_timeout_ms', 3000, '')
        self.udp_max_bytes = self.int_of(props, 'udp_max_bytes', 60000, '')

        self.stuck_service_base_time_ms = self.int_of(props, 'stuck_service_base_time_ms', 300000, '')
        self.stuck_service_remove_enabled = self.bool_of(props, 'stuck_service_remove_enabled', True, '')
        self.stuck_service_alert_enabled = self.bool_of(props, 'stuck_service_alert_enabled', True, '')

        self.trace_activeservice_yellow_time = self.int_of(props, 'trace_activeservice_yellow_time', 3000, '')
        self.trace_activeservice_red_time = self.int_of(props, 'trace_activeservice_red_time', 8000, '')

        self.profile_step_max_keep_in_memory_count = self.int_of(props, 'profile_step_max_keep_in_memory_count', 2048, '')
        self.profile_step_max_count = self.int_of(props, 'profile_step_max_count', 1024, '')

        self.profile_http_querystring_enabled = self.bool_of(props, 'profile_http_querystring_enabled', False, '')
        self.profile_http_header_enabled = self.bool_of(props, 'profile_http_header_enabled', False, '')
        self.profile_http_header_keys = self.string_of_type(props, 'profile_http_header_keys', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')

        self.trace_http_client_ip_header_key = self.string_of(props, 'trace_http_client_ip_header_key', '', '')

        self.xlog_discard_service_patterns = self.string_of_type(props, 'xlog_discard_service_patterns', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')
        self.xlog_discard_service_show_error = self.bool_of(props, 'xlog_discard_service_show_error', True, '')

        self.xlog_sampling_exclude_patterns = self.string_of_type(props, 'xlog_sampling_exclude_patterns', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')

        self.xlog_sampling_enabled = self.bool_of(props, 'xlog_sampling_enabled', False, '')
        self.xlog_sampling_only_profile = self.bool_of(props, 'xlog_sampling_only_profile', False, '')
        self.xlog_sampling_step1_ms = numpy.int32(self.int_of(props, 'xlog_sampling_step1_ms', 100, ''))
        self.xlog_sampling_step1_rate_pct = self.int_of(props, 'xlog_sampling_step1_rate_pct', 2, '')
        self.xlog_sampling_step2_ms = numpy.int32(self.int_of(props, 'xlog_sampling_step2_ms', 500, ''))
        self.xlog_sampling_step2_rate_pct = self.int_of(props, 'xlog_sampling_step2_rate_pct', 7, '')
        self.xlog_sampling_step3_ms = numpy.int32(self.int_of(props, 'xlog_sampling_step3_ms', 1000, ''))
        self.xlog_sampling_step3_rate_pct = self.int_of(props, 'xlog_sampling_step3_rate_pct', 15, '')
        self.xlog_sampling_over_rate_pct = self.int_of(props, 'xlog_sampling_over_rate_pct', 3000, '')

        self.xlog_patterned_sampling_enabled = self.bool_of(props, 'xlog_patterned_sampling_enabled', False, '')
        self.xlog_patterned_sampling_service_patterns = self.string_of_type(props, 'xlog_patterned_sampling_service_patterns', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')
        self.xlog_patterned_sampling_only_profile = self.bool_of(props, 'xlog_patterned_sampling_only_profile', False, '')
        self.xlog_patterned_sampling_step1_ms = numpy.int32(self.int_of(props, 'xlog_patterned_sampling_step1_ms', 100, ''))
        self.xlog_patterned_sampling_step1_rate_pct = self.int_of(props, 'xlog_patterned_sampling_step1_rate_pct', 2, '')
        self.xlog_patterned_sampling_step2_ms = numpy.int32(self.int_of(props, 'xlog_patterned_sampling_step2_ms', 500, ''))
        self.xlog_patterned_sampling_step2_rate_pct = self.int_of(props, 'xlog_patterned_sampling_step2_rate_pct', 7, '')
        self.xlog_patterned_sampling_step3_ms = numpy.int32(self.int_of(props, 'xlog_patterned_sampling_step3_ms', 1000, ''))
        self.xlog_patterned_sampling_step3_rate_pct = self.int_of(props, 'xlog_patterned_sampling_step3_rate_pct', 15, '')
        self.xlog_patterned_sampling_over_rate_pct = self.int_of(props, 'xlog_patterned_sampling_over_rate_pct', 3000, '')

        self.xlog_patterned2_sampling_enabled = self.bool_of(props, 'xlog_patterned2_sampling_enabled', False, '')
        self.xlog_patterned2_sampling_service_patterns = self.string_of_type(props, 'xlog_patterned2_sampling_service_patterns', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')
        self.xlog_patterned2_sampling_only_profile = self.bool_of(props, 'xlog_patterned2_sampling_only_profile', False, '')
        self.xlog_patterned2_sampling_step1_ms = numpy.int32(self.int_of(props, 'xlog_patterned2_sampling_step1_ms', 100, ''))
        self.xlog_patterned2_sampling_step1_rate_pct = self.int_of(props, 'xlog_patterned2_sampling_step1_rate_pct', 2, '')
        self.xlog_patterned2_sampling_step2_ms = numpy.int32(self.int_of(props, 'xlog_patterned2_sampling_step2_ms', 500, ''))
        self.xlog_patterned2_sampling_step2_rate_pct = self.int_of(props, 'xlog_patterned2_sampling_step2_rate_pct', 7, '')
        self.xlog_patterned2_sampling_step3_ms = numpy.int32(self.int_of(props, 'xlog_patterned2_sampling_step3_ms', 1000, ''))
        self.xlog_patterned2_sampling_step3_rate_pct = self.int_of(props, 'xlog_patterned2_sampling_step3_rate_pct', 15, '')
        self.xlog_patterned2_sampling_over_rate_pct = self.int_of(props, 'xlog_patterned2_sampling_over_rate_pct', 3000, '')

        self.xlog_patterned3_sampling_enabled = self.bool_of(props, 'xlog_patterned3_sampling_enabled', False, '')
        self.xlog_patterned3_sampling_service_patterns = self.string_of_type(props, 'xlog_patterned3_sampling_service_patterns', '', ValueType.VT_COMMA_SEPARATED_VALUE, '')
        self.xlog_patterned3_sampling_only_profile = self.bool_of(props, 'xlog_patterned3_sampling_only_profile', False, '')
        self.xlog_patterned3_sampling_step1_ms = numpy.int32(self.int_of(props, 'xlog_patterned3_sampling_step1_ms', 100, ''))
        self.xlog_patterned3_sampling_step1_rate_pct = self.int_of(props, 'xlog_patterned3_sampling_step1_rate_pct', 2, '')
        self.xlog_patterned3_sampling_step2_ms = numpy.int32(self.int_of(props, 'xlog_patterned3_sampling_step2_ms', 500, ''))
        self.xlog_patterned3_sampling_step2_rate_pct = self.int_of(props, 'xlog_patterned3_sampling_step2_rate_pct', 7, '')
        self.xlog_patterned3_sampling_step3_ms = numpy.int32(self.int_of(props, 'xlog_patterned3_sampling_step3_ms', 1000, ''))
        self.xlog_patterned3_sampling_step3_rate_pct = self.int_of(props, 'xlog_patterned3_sampling_step3_rate_pct', 15, '')
        self.xlog_patterned3_sampling_over_rate_pct = self.int_of(props, 'xlog_patterned3_sampling_over_rate_pct', 3000, '')

    @classmethod
    def update_description(cls, key, value, default_value, desc, value_type):
        desc_map[key] = ConfigureDesc(key, value, default_value, desc, value_type)


if __name__ == '__main__':
    config = Configure()
    config.set_trace(True)
    print(config.is_trace())
