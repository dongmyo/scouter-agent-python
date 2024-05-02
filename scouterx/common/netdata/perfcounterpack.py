from scouterx.common.constants.packconstant.packconstants import PERFCOUNTER
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.mapvalue import MapValue
from scouterx.common.netdata.pack import Pack
from scouterx.common.netdata.textvalue import TextValue


class PerfCounterPack(Pack):
    TimeTypeRealTime = 1
    TimeTypeFiveMin = 3

    def __init__(self):
        self.time = 0
        self.obj_name = ""
        self.time_type = 0
        self.data = MapValue()

    def write(self, out):
        out.write_int64(self.time)
        out.write_string(self.obj_name)
        out.write_int8(self.time_type)
        out.write_value(self.data)

    def read(self, data_input_x):
        try:
            self.time = data_input_x.read_int64()
            self.obj_name = data_input_x.read_string()
            self.time_type = data_input_x.read_int8()
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
        return PERFCOUNTER

    def to_string(self) -> str:
        return str(self)
