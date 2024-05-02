from scouterx.common.constants.packconstant.packconstants import XLOG_PROFILE
from scouterx.common.netdata.pack import Pack


class XlogProfilePack(Pack):
    def __init__(self):
        self.time = 0
        self.obj_hash = 0
        self.service = 0
        self.txid = 0
        self.elapsed = 0
        self.profile = bytearray()

    def write(self, out):
        out.write_decimal(self.time)
        out.write_decimal32(self.obj_hash)
        out.write_decimal32(self.service)
        out.write_int64(self.txid)
        out.write_blob(self.profile)

    def read(self, inp):
        # TODO: not yet implemented
        return self, None

    def __str__(self):
        return f"Profile: objHash: {self.obj_hash}"

    @classmethod
    def get_pack_type(cls):
        return XLOG_PROFILE

    def to_string(self) -> str:
        return str(self)
