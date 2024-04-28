from scouterx.common.constants.valueconstant.valueconstants import LIST
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.textvalue import TextValue


class ListValue:
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    @classmethod
    def new_list_value(cls):
        return cls()

    @classmethod
    def new_list_value_with_values(cls, values):
        return cls(values)

    def add(self, value):
        self.values.append(value)
        return self

    def add_int64(self, value):
        self.values.append(DecimalValue.new_decimal_value(value))
        return self

    def add_int32(self, value):
        self.values.append(DecimalValue.new_decimal_value(int(value)))
        return self

    def add_float(self, value):
        self.values.append(Float32Value.new_float_value(value))
        return self

    def add_string(self, value):
        self.values.append(TextValue.new_text_value(value))
        return self

    def add_boolean(self, value):
        self.values.append(BooleanValue.new_boolean_value(value))
        return self

    def get_string(self, index):
        value = self.values[index]
        if isinstance(value, TextValue):
            return str(value)
        return ""

    def get_float(self, index):
        value = self.values[index]
        if isinstance(value, Float32Value):
            return value.value
        return 0.0

    def get_int32(self, index):
        value = self.values[index]
        if isinstance(value, DecimalValue):
            return int(value.value)
        return 0

    def get_int64(self, index):
        value = self.values[index]
        if isinstance(value, DecimalValue):
            return value.value
        return 0

    def get_boolean(self, index):
        value = self.values[index]
        if isinstance(value, BooleanValue):
            return value.value
        return False

    def size(self):
        return len(self.values)

    def write(self, data_output):
        try:
            data_output.write_decimal(len(self.values))
            for value in self.values:
                data_output.write_value(value)
            return None
        except Exception as e:
            return e

    def read(self, data_input):
        size, err = data_input.read_decimal()
        if err:
            return None, err
        self.values = []
        for _ in range(size):
            value, err = data_input.read_value()
            if err:
                return None, err
            self.values.append(value)
        return self, None

    @classmethod
    def get_value_type(cls):
        return LIST

    def __str__(self):
        result = "List Value: ["
        for index, value in enumerate(self.values):
            if value is None:
                result += f"{index}: None, "
            else:
                result += f"{index}: {value}, "
        result = result.rstrip(", ") + "]"
        return result
