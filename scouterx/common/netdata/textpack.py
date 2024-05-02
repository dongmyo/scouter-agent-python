import numpy

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

    def write(self, out):
        out.write_string(str(self.xtype))
        out.write_int32(numpy.int32(self.hash))
        out.write_string(self.text)

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
