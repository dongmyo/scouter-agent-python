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

    def write(self, data_output_x):
        try:
            super().write(data_output_x)
            data_output_x.write_decimal(self.txid)
            data_output_x.write_decimal32(self.hash)
            data_output_x.write_decimal32(self.elapsed)
            data_output_x.write_decimal32(self.cpu_time)
            data_output_x.write_decimal32(self.error)
            data_output_x.write_uint8(self.opt)
            if self.opt == 1:
                data_output_x.write_string(self.address)
            return None
        except Exception as e:
            return e


def new_api_call_step():
    return ApiCallStep()
