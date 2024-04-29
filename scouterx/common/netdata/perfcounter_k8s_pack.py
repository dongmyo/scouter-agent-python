from scouterx.common.constants.packconstant.packconstants import PERFCOUNTER_K8S
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.mapvalue import MapValue
from scouterx.common.netdata.pack import Pack
from scouterx.common.netdata.textvalue import TextValue


class PerfCounterK8SPack(Pack):
    def __init__(self):
        self.time = 0
        self.site_id = ""
        self.cluster = ""
        self.namespace = ""
        self.node_name = ""
        self.daemonset_name = ""
        self.deployment_name = ""
        self.pod_name = ""
        self.container_name = ""
        self.obj_name = ""
        self.timetype = 0
        self.metric_level = 0
        self.data = MapValue()

    def write(self, out):
        try:
            out.write_int64(self.time)
            out.write_string(self.site_id)
            out.write_string(self.cluster)
            out.write_string(self.namespace)
            out.write_string(self.node_name)
            out.write_string(self.daemonset_name)
            out.write_string(self.deployment_name)
            out.write_string(self.pod_name)
            out.write_string(self.container_name)
            out.write_string(self.obj_name)
            out.write_int8(self.timetype)
            out.write_int8(self.metric_level)
            out.write_value(self.data)
        except Exception as e:
            return e

    def read(self, data_input_x):
        try:
            self.time = data_input_x.read_int64()
            self.site_id = data_input_x.read_string()
            self.cluster = data_input_x.read_string()
            self.namespace = data_input_x.read_string()
            self.node_name = data_input_x.read_string()
            self.daemonset_name = data_input_x.read_string()
            self.deployment_name = data_input_x.read_string()
            self.pod_name = data_input_x.read_string()
            self.container_name = data_input_x.read_string()
            self.obj_name = data_input_x.read_string()
            self.timetype = data_input_x.read_int8()
            self.metric_level = data_input_x.read_int8()
            value = data_input_x.read_value()
            self.data = value
            return self, None
        except Exception as e:
            return None, e

    def put(self, key, any_value):
        if isinstance(any_value, int):
            self.data.put(key, DecimalValue(any_value))
        elif isinstance(any_value, float):
            self.data.put(key, Float32Value(any_value))
        elif isinstance(any_value, str):
            self.data.put(key, TextValue(any_value))
        elif isinstance(any_value, bool):
            self.data.put(key, BooleanValue(any_value))
        else:
            self.data.put(key, any_value)

    def __str__(self):
        return self.data.__str__()

    @classmethod
    def get_pack_type(cls):
        return PERFCOUNTER_K8S

    def to_string(self) -> str:
        return str(self)
