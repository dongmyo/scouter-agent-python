from scouterx.common.constants.valueconstant.valueconstants import DOUBLE


class DoubleValue:
    def __init__(self, value=0.0):
        self.value = value

    @classmethod
    def new_double_value(cls, value):
        return cls(value)

    @classmethod
    def new_double_empty_value(cls):
        return cls()

    def read(self, data_input):
        try:
            self.value, err = data_input.read_float64()
            return self, err
        except Exception as e:
            return None, e

    def write(self, data_output):
        try:
            return None, data_output.write_float64(self.value)
        except Exception as e:
            return e

    @classmethod
    def get_value_type(cls):
        return DOUBLE

    def __str__(self):
        return "{:.3f}".format(self.value)
