from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.step import SingleStep, METHOD


class DumpStep(SingleStep):
    def __init__(self):
        super().__init__()
        self.stacks = []
        self._threadId = 0
        self._threadName = ""
        self._threadState = ""
        self._lockOwnerId = 0
        self._lockName = ""
        self._lockOwnerName = ""

    @classmethod
    def get_step_type(cls):
        return METHOD

    def write(self, out):
        # First write the inherited SingleStep data
        error = super().write(out)
        if error:
            return error

        # Then write the specific fields of DumpStep
        try:
            out.write_int32_array(self.stacks)
            out.write_int64(self._threadId)
            out.write_string(self._threadName)
            out.write_string(self._threadState)
            out.write_int64(self._lockOwnerId)
            out.write_string(self._lockName)
            out.write_string(self._lockOwnerName)
        except Exception as e:
            return e

        return None


if __name__ == '__main__':
    out = DataOutputX()
    step = DumpStep()
    step.stacks = [1, 2, 3, 4]
    step._threadId = 123456789
    step._threadName = "Main Thread"
    step._threadState = "RUNNING"
    step._lockOwnerId = 987654321
    step._lockName = "mutexLock"
    step._lockOwnerName = "Owner Thread"
    error = step.write(out)
    if error:
        print("An error occurred:", error)
