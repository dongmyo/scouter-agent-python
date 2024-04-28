from scouterx.common.constants.valueconstant.valueconstants import BOOLEAN


class BooleanValue:
    def __init__(self, value=False):
        self.value = value

    @classmethod
    def new_boolean_value(cls, value):
        return cls(value)

    @classmethod
    def new_boolean_empty_value(cls):
        return cls()

    @classmethod
    def get_value_type(cls):
        return BOOLEAN

    def read(self, data_input):
        try:
            self.value, err = data_input.read_boolean()
            return self, err
        except Exception as e:
            return None, e

    def write(self, data_output):
        try:
            data_output.write_boolean(self.value)
            return None
        except Exception as e:
            return e

    def __str__(self):
        return str(self.value).lower()
