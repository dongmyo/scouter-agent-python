from scouterx.common.netdata.step import APICALL, SingleStep


class ApiCallStep(SingleStep):
    def __init__(self):
        super().__init__()
        self.txid = 0
        self.hash = 0
        self.elapsed = 0
        self.cpu_time = 0
        self.error = 0
        self.opt = 0
        self.address = ""

    @classmethod
    def get_step_type(cls):
        return APICALL  # APICALL should be defined as a constant representing the type byte

    def write(self, out):
        super().write(out)
        out.write_decimal(self.txid)
        out.write_decimal32(self.hash)
        out.write_decimal32(self.elapsed)
        out.write_decimal32(self.cpu_time)
        out.write_decimal32(self.error)
        out.write_uint8(self.opt)
        if self.opt == 1:
            out.write_string(self.address)


def new_api_call_step():
    return ApiCallStep()
