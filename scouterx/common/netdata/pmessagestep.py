from dataclasses import dataclass, field

import numpy

from scouterx.common.netdata.step import PARAMETERIZED_MESSAGE, SingleStep

delimETX = 3

PMSG_DEBUG = 0
PMSG_INFO = 1
PMSG_WARN = 2
PMSG_ERROR = 3
PMSG_FATAL = 4


@dataclass
class PMessageStep:
    single_step: SingleStep
    hash: int = 0
    elapsed: int = 0
    level: int = 0
    param_string: str = ""
    temp_map: dict = field(default_factory=dict)

    def __init__(self, start_time):
        self.StartTime = start_time
        self.temp_map = {}

    @classmethod
    def get_step_type(cls):
        return PARAMETERIZED_MESSAGE

    def write(self, out):
        self.single_step.write(out)
        out.write_decimal32(self.hash)
        out.write_decimal32(self.elapsed)
        out.write_decimal32(numpy.int32(self.level))
        out.write_string(self.param_string)

    def set_message(self, hash, *params):
        self.hash = hash
        parts = []
        for s in params:
            parts.append(s + chr(delimETX))
        self.param_string = ''.join(parts)
