from dataclasses import dataclass, field

from scouterx.common.netdata.step import SingleStep, THREAD_CALL_POSSIBLE


@dataclass
class AsyncServiceStep:
    single_step: SingleStep
    txid: int = 0
    hash: int = 0
    elapsed: int = 0

    def __init__(self):
        self.single_step = SingleStep()

    @classmethod
    def get_step_type(cls):
        return THREAD_CALL_POSSIBLE

    def write(self, out):
        self.single_step.write(out)
        out.write_decimal(self.txid)
        out.write_decimal32(self.hash)
        out.write_decimal32(self.elapsed)
        out.write_uint8(1)
