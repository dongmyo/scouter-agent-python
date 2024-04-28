from enum import Enum

from scouterx.common.constants.packconstant.packconstants import ALERT
from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.mapvalue import MapValue


class AlertLevel(Enum):
    INFO = 0
    WARN = 1
    ERROR = 2
    FATAL = 3


class AlertPack:
    def __init__(self):
        self.time = 0
        self.obj_type = ''
        self.obj_hash = 0
        self.level = AlertLevel.INFO
        self.title = ''
        self.message = ''
        self.tags = MapValue()

    def write(self, output: DataOutputX):
        output.write_int64(self.time)
        output.write_uint8(self.level.value)
        output.write_string(self.obj_type)
        output.write_int32(self.obj_hash)
        output.write_string(self.title)
        output.write_string(self.message)
        output.write_value(self.tags)

    def read(self, input: DataInputX):
        # Placeholder for read logic
        pass

    def __str__(self):
        return f"AlertPack: title: {self.title} message: {self.message}"

    @classmethod
    def get_pack_type(cls):
        return ALERT


if __name__ == '__main__':
    pack = AlertPack()
    pack.title = "Example Alert"
    pack.message = "This is an alert."
    output = DataOutputX()
    pack.write(output)
    print(pack)
