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
        if super().write(out):
            return True

        if out.write_decimal32(self.hash):
            return True
        if out.write_decimal32(self.elapsed):
            return True
        if out.write_decimal32(self.cpu_time):
            return True

        return False
