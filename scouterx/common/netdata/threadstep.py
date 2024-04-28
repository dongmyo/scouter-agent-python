from dataclasses import dataclass, field

from scouterx.common.netdata.step import SingleStep, THREAD_CALL_POSSIBLE


@dataclass
class AsyncServiceStep:
    SingleStep: 'SingleStep'
    Txid: int = 0
    Hash: int = 0
    Elapsed: int = 0

    def __init__(self):
        self.SingleStep = SingleStep()

    @classmethod
    def get_step_type(cls):
        return THREAD_CALL_POSSIBLE

    def write(self, out):
        try:
            self.SingleStep.write(out)
            out.write_decimal(self.Txid)
            out.write_decimal32(self.Hash)
            out.write_decimal32(self.Elapsed)
            out.write_uint8(1)
        except Exception as e:
            return e
