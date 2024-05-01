import time

import numpy

from scouterx.common.netdata.xlogpack import XlogType, XlogPack
from scouterx.common.util.ip_util import ip_to_bytes
from scouterx.common.util.keygen.keygen import KeyGen
from scouterx.netio.dataproxy import send_desc, send_login, send_hashed_message
from scouterx.netio.profilecollector import ProfileCollector


class TraceContext:
    def __init__(self, noop=False):
        self.closed = False
        self.noop = noop
        self.last_method = ""
        self.is_stream = False

        self.inherit = False
        self.inherit_start_time = time.time()

        self.goid = 0
        self.parent = None
        self.profile = ProfileCollector(self)
        self.profile_count = 0
        self.profile_size = 0

        self.txid = -1 if noop else KeyGen.get_instance().next()
        self.gxid = 0
        self.xtype = XlogType()

        self.start_time = time.time()

        self.service_hash = 0
        self.service_name = ""
        self.remote_ip = ""

        self.error = 0
        self.http_method = ""
        self.http_query = ""
        self.http_content_type = ""

        self.sql_count = 0
        self.sql_time = 0
        self.sql_text = ""

        self.status = 0
        self.apicall_name = ""
        self.apicall_count = 0
        self.apicall_time = 0
        self.apicall_target = ""

        self.userid = 0
        self.user_agent = 0
        self.user_agent_string = ""
        self.referer = 0

        self.is_child_tx = False
        self.caller = 0
        self.callee = 0
        self.caller_obj_hash = 0

        self.login = ""
        self.desc = ""

        self.text1 = ""
        self.text2 = ""
        self.text3 = ""
        self.text4 = ""
        self.text5 = "NoopTctx" if noop else ""

    def to_xlog(self, discard_type, elapsed):
        xlog = XlogPack()
        xlog.elapsed = elapsed
        xlog.service = self.service_hash
        xlog.xtype = self.xtype
        xlog.txid = self.txid
        xlog.gxid = self.gxid
        xlog.caller = self.caller
        xlog.thread_name_hash = send_hashed_message(str(self.gxid))
        xlog.sql_count = self.sql_count
        xlog.sql_time = self.sql_time
        xlog.ipaddr = ip_to_bytes(self.remote_ip)
        xlog.userid = self.userid
        xlog.has_dump = 0
        xlog.error = self.error

        xlog.status = self.status

        xlog.discard_type = discard_type
        xlog.profile_size = numpy.int32(self.profile_size)
        xlog.profile_count = numpy.int32(self.profile_count)
        xlog.user_agent = self.user_agent
        xlog.referer = self.referer

        xlog.apicall_count = self.apicall_count
        xlog.apicall_time = self.apicall_time

        if self.login:
            xlog.login = send_login(self.login)
        if self.desc:
            xlog.desc = send_desc(self.desc)
        xlog.text1 = self.text1
        xlog.text2 = self.text2
        xlog.text3 = self.text3
        xlog.text4 = self.text4
        xlog.text5 = self.text5

        return xlog
