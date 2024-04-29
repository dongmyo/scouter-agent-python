from scouterx.common.constants.packconstant.packconstants import XLOG
from scouterx.common.netdata.pack import Pack

XTYPE_WEB_SERVICE = 0
XTYPE_APP_SERVICE = 1
XTYPE_BACK_THREAD = 2
XTYPE_BACK_THREAD2 = 4
XTYPE_ZIPKIN_SPAN = 5
XTYPE_UNKNOWN = 99

XLOG_DISCARD_NONE = 1
XLOG_DISCARD_ALL = 2
XLOG_DISCARD_PROFILE = 3
XLOG_DISCARD_ALL_FORCE = 4
XLOG_DISCARD_PROFILE_FORCE = 5


# type XlogType uint8
class XlogType:
    def __init__(self, value: int = 0):
        if not (0 <= value <= 255):
            raise ValueError("XlogType must be between 0 and 255")
        self.value = value


# type XlogDiscardType uint8
class XlogDiscardType:
    def __init__(self, value: int = 0):
        if not (0 <= value <= 255):
            raise ValueError("XlogDiscardType must be between 0 and 255")
        self.value = value


class XlogPack(Pack):
    def __init__(self):
        self.EndTime = 0
        self.ObjHash = 0
        self.Service = 0
        self.Txid = 0
        self.ThreadNameHash = 0
        self.Caller = 0
        self.Gxid = 0
        self.Elapsed = 0
        self.Error = 0
        self.Cpu = 0
        self.SqlCount = 0
        self.SqlTime = 0
        self.Ipaddr = bytearray()
        self.Kbytes = 0
        self.Status = 0
        self.Userid = 0
        self.UserAgent = 0
        self.Referer = 0
        self.Group = 0
        self.ApicallCount = 0
        self.ApicallTime = 0
        self.CountryCode = ''
        self.City = 0
        self.XType = 0
        self.Login = 0
        self.Desc = 0
        self.WebHash = 0
        self.WebTime = 0
        self.HasDump = 0
        self.Text1 = ''
        self.Text2 = ''
        self.QueuingHostHash = 0
        self.QueuingTime = 0
        self.Queuing2ndHostHash = 0
        self.Queuing2ndTime = 0
        self.Text3 = ''
        self.Text4 = ''
        self.Text5 = ''
        self.ProfileCount = 0
        self.B3Mode = False
        self.ProfileSize = 0
        self.DiscardType = 0
        self.IgnoreGlobalConsequentSampling = False

    def is_driving(self):
        return self.Gxid == self.Txid or self.Gxid == 0

    def write(self, out):
        try:
            out.write_decimal(self.EndTime)
            out.write_decimal32(self.ObjHash)
            out.write_decimal32(self.Service)
            out.write_int64(self.Txid)
            out.write_int64(self.Caller)
            out.write_int64(self.Gxid)
            out.write_decimal32(self.Elapsed)
            out.write_decimal32(self.Error)
            out.write_decimal32(self.Cpu)
            out.write_decimal32(self.SqlCount)
            out.write_decimal32(self.SqlTime)
            out.write_blob(self.Ipaddr)
            out.write_decimal32(self.Kbytes)
            out.write_decimal32(self.Status)
            out.write_decimal(self.Userid)
            out.write_decimal32(self.UserAgent)
            out.write_decimal32(self.Referer)
            out.write_decimal32(self.Group)
            out.write_decimal32(self.ApicallCount)
            out.write_decimal32(self.ApicallTime)
            out.write_string(self.CountryCode)
            out.write_decimal32(self.City)
            out.write_uint8(self.XType)
            out.write_decimal32(self.Login)
            out.write_decimal32(self.Desc)
            out.write_decimal32(self.WebHash)
            out.write_decimal32(self.WebTime)
            out.write_uint8(self.HasDump)
            out.write_decimal32(self.ThreadNameHash)
            out.write_string(self.Text1)
            out.write_string(self.Text2)
            out.write_decimal32(self.QueuingHostHash)
            out.write_decimal32(self.QueuingTime)
            out.write_decimal32(self.Queuing2ndHostHash)
            out.write_decimal32(self.Queuing2ndTime)
            out.write_string(self.Text3)
            out.write_string(self.Text4)
            out.write_string(self.Text5)
            out.write_decimal32(self.ProfileCount)
            out.write_boolean(self.B3Mode)
            out.write_decimal32(self.ProfileSize)
            out.write_uint8(self.DiscardType)
            out.write_boolean(self.IgnoreGlobalConsequentSampling)
        except Exception as e:
            return e

    def read(self, inp):
        # TODO: not yet implemented
        return self, None

    def __str__(self):
        return (f"XLOG: objHash: {self.ObjHash}, service: {self.Service}, txid: {self.Txid}, "
                f"elapsed: {self.Elapsed}, error: {self.Error}")

    @classmethod
    def get_pack_type(cls):
        return XLOG

    def to_string(self) -> str:
        return str(self)
