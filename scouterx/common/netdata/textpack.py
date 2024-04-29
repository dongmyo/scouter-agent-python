from scouterx.common.constants.packconstant.packconstants import TEXT
from scouterx.common.netdata.pack import Pack


class TextPack(Pack):
    def __init__(self, xtype=None, hash_value=0, text=''):
        self.xtype = xtype
        self.hash = hash_value
        self.text = text

    @classmethod
    def new_text_pack(cls):
        return cls()

    def write(self, data_output):
        try:
            data_output.write_string(str(self.xtype))
            data_output.write_int32(self.hash)
            data_output.write_string(self.text)
            return None
        except Exception as e:
            return e

    def read(self, data_input):
        # TODO not yet implemented
        raise NotImplementedError("Read method not implemented.")

    def __str__(self):
        return f"{self.xtype} hash: {self.hash} text: {self.text}"

    @classmethod
    def get_pack_type(cls):
        return TEXT

    def to_string(self) -> str:
        return str(self)
