from scouterx.common.constants.valueconstant.valueconstants import TEXT


class TextValue:
    def __init__(self, value=''):
        self.value = value

    @classmethod
    def new_text_value(cls, value):
        return cls(value)

    @classmethod
    def new_text_empty_value(cls):
        return cls()

    def read(self, data_input):
        try:
            self.value, err = data_input.read_string()
            return self, err
        except Exception as e:
            return None, e

    def write(self, out):
        out.write_string(self.value)

    @classmethod
    def get_value_type(cls):
        return TEXT

    def __str__(self):
        return self.value
