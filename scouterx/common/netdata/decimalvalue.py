from scouterx.common.constants.valueconstant.valueconstants import DECIMAL


class DecimalValue:
    def __init__(self, value=0):
        self.value = value

    @classmethod
    def new_decimal_value(cls, value):
        return cls(value)

    @classmethod
    def new_decimal_empty_value(cls):
        return cls()

    def read(self, data_input):
        try:
            self.value, err = data_input.read_decimal()
            return self, err
        except Exception as e:
            return None, e

    def write(self, out):
        out.write_decimal(self.value)

    @classmethod
    def get_value_type(cls):
        return DECIMAL

    def __str__(self):
        return str(self.value)
