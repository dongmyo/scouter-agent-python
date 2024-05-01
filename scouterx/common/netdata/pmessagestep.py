from dataclasses import dataclass, field

import numpy

from scouterx.common.netdata.step import PARAMETERIZED_MESSAGE

delimETX = 3

PMSG_DEBUG = 0
PMSG_INFO = 1
PMSG_WARN = 2
PMSG_ERROR = 3
PMSG_FATAL = 4


@dataclass
class PMessageStep:
    SingleStep: 'SingleStep'  # Assuming SingleStep is another class that will be defined elsewhere.
    Hash: int = 0
    Elapsed: int = 0
    Level: int = 0
    paramString: str = ""
    tempMap: dict = field(default_factory=dict)

    def __init__(self, start_time):
        self.StartTime = start_time
        self.tempMap = {}

    @classmethod
    def get_step_type(cls):
        return PARAMETERIZED_MESSAGE

    def write(self, out):
        try:
            self.SingleStep.write(out)
            out.write_decimal32(self.Hash)
            out.write_decimal32(self.Elapsed)
            out.write_decimal32(numpy.int32(self.Level))
            out.write_string(self.paramString)
        except Exception as e:
            return e

    def set_message(self, hash, *params):
        self.Hash = hash
        parts = []
        for s in params:
            parts.append(s + chr(delimETX))
        self.paramString = ''.join(parts)
