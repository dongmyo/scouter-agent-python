from scouterx.common.constants.valueconstant.valueconstants import FLOAT


class Float32Value:
    def __init__(self, value=0.0):
        self.value = value

    @classmethod
    def new_float_value(cls, value):
        return cls(value)

    @classmethod
    def new_float_empty_value(cls):
        return cls()

    def read(self, data_input):
        try:
            self.value, err = data_input.read_float32()
            return self, err
        except Exception as e:
            return None, e

    def write(self, data_output):
        try:
            return None, data_output.write_float32(self.value)
        except Exception as e:
            return e

    @classmethod
    def get_value_type(cls):
        return FLOAT

    def __str__(self):
        return "{:.3f}".format(self.value)
