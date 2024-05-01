import numpy

from scouterx.common.constants.packconstant.packconstants import XLOG
from scouterx.common.netdata.dataoutputx import DataOutputX
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

    def __int__(self):
        return self.value


# type XlogDiscardType uint8
class XlogDiscardType:
    def __init__(self, value: int = 0):
        if not (0 <= value <= 255):
            raise ValueError("XlogDiscardType must be between 0 and 255")
        self.value = value

    def __int__(self):
        return self.value


class XlogPack(Pack):
    def __init__(self):
        self.end_time = 0
        self.obj_hash = 0
        self.service = 0
        self.txid = 0
        self.thread_name_hash = 0
        self.caller = 0
        self.gxid = 0
        self.elapsed = 0
        self.error = 0
        self.cpu = 0
        self.sql_count = 0
        self.sql_time = 0
        self.ipaddr = bytearray()
        self.kbytes = 0
        self.status = 0
        self.userid = 0
        self.user_agent = 0
        self.referer = 0
        self.group = 0
        self.apicall_count = 0
        self.apicall_time = 0
        self.country_code = ''
        self.city = 0
        self.xtype = XlogType()
        self.login = 0
        self.desc = 0
        self.web_hash = 0
        self.web_time = 0
        self.has_dump = 0
        self.text1 = ''
        self.text2 = ''
        self.queuing_host_hash = 0
        self.queuing_time = 0
        self.queuing_2nd_host_hash = 0
        self.queuing_2nd_time = 0
        self.text3 = ''
        self.text4 = ''
        self.text5 = ''
        self.profile_count = 0
        self.b3_mode = False
        self.profile_size = 0
        self.discard_type = 0
        self.ignore_global_consequent_sampling = False

    def is_driving(self):
        return self.gxid == self.txid or self.gxid == 0

    def write(self, out):
        try:
            o = DataOutputX()

            o.write_decimal(self.end_time)
            o.write_decimal32(self.obj_hash)
            o.write_decimal32(self.service)
            o.write_int64(self.txid)
            o.write_int64(self.caller)
            o.write_int64(self.gxid)
            o.write_decimal32(self.elapsed)
            o.write_decimal32(self.error)
            o.write_decimal32(self.cpu)
            o.write_decimal32(self.sql_count)
            o.write_decimal32(self.sql_time)
            o.write_blob(self.ipaddr)
            o.write_decimal32(self.kbytes)
            o.write_decimal32(self.status)
            o.write_decimal(self.userid)
            o.write_decimal32(self.user_agent)
            o.write_decimal32(self.referer)
            o.write_decimal32(self.group)
            o.write_decimal32(self.apicall_count)
            o.write_decimal32(self.apicall_time)
            o.write_string(self.country_code)
            o.write_decimal32(self.city)
            o.write_uint8(numpy.uint8(self.xtype))
            o.write_decimal32(self.login)
            o.write_decimal32(self.desc)
            o.write_decimal32(self.web_hash)
            o.write_decimal32(self.web_time)
            o.write_uint8(self.has_dump)
            o.write_decimal32(self.thread_name_hash)
            o.write_string(self.text1)
            o.write_string(self.text2)
            o.write_decimal32(self.queuing_host_hash)
            o.write_decimal32(self.queuing_time)
            o.write_decimal32(self.queuing_2nd_host_hash)
            o.write_decimal32(self.queuing_2nd_time)
            o.write_string(self.text3)
            o.write_string(self.text4)
            o.write_string(self.text5)
            o.write_decimal32(self.profile_count)
            o.write_boolean(self.b3_mode)
            o.write_decimal32(self.profile_size)
            o.write_uint8(numpy.uint8(self.discard_type))
            o.write_boolean(self.ignore_global_consequent_sampling)

            out.write_blob(o.get_bytes())
        except Exception as e:
            return e

    def read(self, inp):
        # TODO: not yet implemented
        return self, None

    def __str__(self):
        return (f"XLOG: objHash: {self.obj_hash}, service: {self.service}, txid: {self.txid}, "
                f"elapsed: {self.elapsed}, error: {self.error}")

    @classmethod
    def get_pack_type(cls):
        return XLOG

    def to_string(self) -> str:
        return str(self)
