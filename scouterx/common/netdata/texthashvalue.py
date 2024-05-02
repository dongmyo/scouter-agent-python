from scouterx.common.constants.valueconstant.valueconstants import TEXT_HASH


class TextHashValue:
    def __init__(self, value=0):
        self.value = value

    @classmethod
    def new_text_hash_value(cls, value):
        return cls(value)

    @classmethod
    def new_text_hash_empty_value(cls):
        return cls()

    def read(self, data_input):
        try:
            self.value, err = data_input.read_int32()
            return self, err
        except Exception as e:
            return None, e

    def write(self, out):
        out.write_int32(self.value)

    @classmethod
    def get_value_type(cls):
        return TEXT_HASH

    def __str__(self):
        return str(self.value)
