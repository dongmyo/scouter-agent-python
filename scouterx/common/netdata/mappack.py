import numpy

from scouterx.common.constants.packconstant.packconstants import MAP
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.listvalue import ListValue
from scouterx.common.netdata.pack import Pack
from scouterx.common.netdata.textvalue import TextValue
from scouterx.common.netdata.value import Value


class MapPack(Pack):
    def __init__(self):
        self.table = {}

    def is_empty(self):
        return len(self.table) == 0

    def new_list(self, key):
        lst = ListValue()
        self.put(key, lst)
        return lst

    def contains_key(self, key):
        return key in self.table

    def read(self, data_input_x):
        count, err = data_input_x.read_decimal()
        for _ in range(count):
            key, err = data_input_x.read_string()
            value, err = data_input_x.read_value()
            self.table[key] = value
        return self, err

    def write(self, data_output_x):
        err = data_output_x.write_decimal(len(self.table))
        for key, value in self.table.items():
            err = data_output_x.write_string(key)
            err = data_output_x.write_value(value)
        return err

    @classmethod
    def get_pack_type(cls):
        return MAP

    def put(self, key, any_value):
        if isinstance(any_value, str):
            self.table[key] = TextValue(any_value)
        elif isinstance(any_value, int):
            self.table[key] = DecimalValue(numpy.int64(any_value))
        elif isinstance(any_value, bool):
            self.table[key] = BooleanValue(any_value)
        elif isinstance(any_value, Value):
            self.table[key] = any_value
        elif isinstance(any_value, float):
            self.table[key] = Float32Value(any_value)
        elif isinstance(any_value, numpy.int32):
            self.table[key] = DecimalValue(any_value)
        elif isinstance(any_value, numpy.int64):
            self.table[key] = DecimalValue(any_value)

    def get_string(self, key):
        if isinstance(self.table.get(key), TextValue):
            return self.table[key].value
        return ""

    def get_boolean(self, key):
        if isinstance(self.table.get(key), BooleanValue):
            return self.table[key].value
        return False

    def get_int8(self, key):
        if isinstance(self.table.get(key), DecimalValue):
            return numpy.int8(self.table[key].value)
        return numpy.int8(0)

    def get_int16(self, key):
        if isinstance(self.table.get(key), DecimalValue):
            return numpy.int16(self.table[key].value)
        return numpy.int16(0)

    def get_int32(self, key):
        if isinstance(self.table.get(key), DecimalValue):
            return numpy.int32(self.table[key].value)
        return numpy.int32(0)

    def get_int64(self, key):
        if isinstance(self.table.get(key), DecimalValue):
            return numpy.int64(self.table[key].value)
        return numpy.int64(0)

    def __str__(self):
        str_repr = "map value \n"
        for k, v in self.table.items():
            str_repr += f"key: {k} value: {v}\n"
        return str_repr

    def to_string(self) -> str:
        return str(self)
