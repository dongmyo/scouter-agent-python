from scouterx.common.netdata.step import METHOD, SingleStep


class MethodStep(SingleStep):
    def __init__(self, start_time, hash_code, elapsed, cpu_time):
        super().__init__(start_time)
        self.hash = hash_code
        self.elapsed = elapsed
        self.cpu_time = cpu_time

    @classmethod
    def get_step_type(cls):
        return METHOD

    def write(self, out):
        super().write(out)
        out.write_decimal32(self.hash)
        out.write_decimal32(self.elapsed)
        out.write_decimal32(self.cpu_time)
