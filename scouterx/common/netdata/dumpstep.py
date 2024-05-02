from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.step import SingleStep, METHOD


class DumpStep(SingleStep):
    def __init__(self):
        super().__init__()
        self.stacks = []
        self._thread_id = 0
        self._thread_name = ""
        self._thread_state = ""
        self._lock_owner_id = 0
        self._lock_name = ""
        self._lock_owner_name = ""

    @classmethod
    def get_step_type(cls):
        return METHOD

    def write(self, out):
        super().write(out)

        out.write_int32_array(self.stacks)
        out.write_int64(self._thread_id)
        out.write_string(self._thread_name)
        out.write_string(self._thread_state)
        out.write_int64(self._lock_owner_id)
        out.write_string(self._lock_name)
        out.write_string(self._lock_owner_name)


if __name__ == '__main__':
    out = DataOutputX()
    step = DumpStep()
    step.stacks = [1, 2, 3, 4]
    step._thread_id = 123456789
    step._thread_name = "Main Thread"
    step._thread_state = "RUNNING"
    step._lock_owner_id = 987654321
    step._lock_name = "mutexLock"
    step._lock_owner_name = "Owner Thread"
    step.write(out)
