from scouterx.common.constants.packconstant.packconstants import XLOG_PROFILE


class XlogProfilePack:
    def __init__(self):
        self.Time = 0
        self.ObjHash = 0
        self.Service = 0
        self.Txid = 0
        self.Elapsed = 0
        self.Profile = bytearray()

    def write(self, out):
        try:
            out.write_decimal(self.Time)
            out.write_decimal32(self.ObjHash)
            out.write_decimal32(self.Service)
            out.write_int64(self.Txid)
            out.write_blob(self.Profile)
        except Exception as e:
            return e

    def read(self, inp):
        # TODO: not yet implemented
        return self, None

    def __str__(self):
        return f"Profile: objHash: {self.ObjHash}"

    @classmethod
    def get_pack_type(cls):
        return XLOG_PROFILE
