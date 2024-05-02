from scouterx.common.constants.valueconstant.valueconstants import NULL


class NilValue:
    def __init__(self, value=None):
        self.value = value

    @classmethod
    def new_nil_value(cls):
        return cls()

    def read(self, data_input):
        # Assuming `read` should do nothing but return the existing instance and no error
        return self, None

    def write(self, out):
        pass

    def get_value_type(self):
        return NULL

    def __str__(self):
        return "nil"
