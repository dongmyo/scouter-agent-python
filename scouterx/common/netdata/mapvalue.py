from scouterx.common.constants.valueconstant.valueconstants import MAP
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.textvalue import TextValue
from scouterx.common.netdata.value import Value


class MapValue:
    def __init__(self):
        self.table = {}

    @classmethod
    def new_map_value(cls):
        return cls()

    def is_empty(self):
        return len(self.table) == 0

    def contains_key(self, key):
        return key in self.table

    def read(self, data_input):
        size, err = data_input.read_decimal()
        if err:
            return None, err
        for _ in range(size):
            key, err = data_input.read_string()
            if err:
                return None, err
            value, err = data_input.read_value()
            if err:
                return None, err
            self.table[key] = value
        return self, None

    def write(self, out):
        out.write_decimal(len(self.table))
        for key, value in self.table.items():
            out.write_string(key)
            out.write_value(value)

    @classmethod
    def get_value_type(cls):
        return MAP

    def put(self, key, value):
        if isinstance(value, str):
            self.table[key] = TextValue.new_text_value(value)
        elif isinstance(value, bool):
            self.table[key] = BooleanValue.new_boolean_value(value)
        elif isinstance(value, int):  # handling all int as int64 for simplicity
            self.table[key] = DecimalValue.new_decimal_value(value)
        elif isinstance(value, float):
            # assuming float means float32 here, adjust if needed
            self.table[key] = Float32Value.new_float_value(value)
        elif isinstance(value, Value):
            self.table[key] = value

    def get_string(self, key):
        value = self.table.get(key)
        if isinstance(value, TextValue):
            return value.value
        return ""

    def get_boolean(self, key):
        value = self.table.get(key)
        if isinstance(value, BooleanValue):
            return value.value
        return False

    def get_int8(self, key):
        return int(self.get_int64(key) & 0xff)

    def get_int16(self, key):
        return int(self.get_int64(key) & 0xffff)

    def get_int32(self, key):
        return int(self.get_int64(key) & 0xffffffff)

    def get_int64(self, key):
        value = self.table.get(key)
        if isinstance(value, DecimalValue):
            return value.value
        return 0

    def __str__(self):
        result = "Map Value:\n"
        for key, value in self.table.items():
            result += f"key: {key}, value: {value}\n"
        return result
