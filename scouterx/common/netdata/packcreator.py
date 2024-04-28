from scouterx.common.constants.packconstant.packconstants import *
from scouterx.common.netdata.alertpack import AlertPack
from scouterx.common.netdata.mappack import MapPack
from scouterx.common.netdata.objectpack import ObjectPack2
from scouterx.common.netdata.perfcounterpack import PerfCounterPack
from scouterx.common.netdata.textpack import TextPack


def create_pack(pack_type):
    if pack_type == MAP:
        return MapPack()
    elif pack_type == TEXT:
        return TextPack()
    elif pack_type == PERFCOUNTER:
        return PerfCounterPack()
    elif pack_type == OBJECT:
        return ObjectPack2()
    elif pack_type == ALERT:
        return AlertPack()
    else:
        return None
