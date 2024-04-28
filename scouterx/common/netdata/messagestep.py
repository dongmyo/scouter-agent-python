from scouterx.common.netdata.step import SingleStep, MESSAGE


class MessageStep(SingleStep):
    def __init__(self, message, start_time):
        super().__init__(start_time)
        self.message = message

    @classmethod
    def get_step_type(cls):
        return MESSAGE

    def write(self, out):
        super().write(out)
        return out.write_string(self.message)
