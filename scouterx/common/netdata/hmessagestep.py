from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.step import SingleStep, HASHED_MESSAGE


class HashedMessageStep(SingleStep):
    def __init__(self, hash, time):
        super().__init__()
        self.hash = hash
        self.time = time
        self.value = 0  # Initialize Value to zero or any default

    @classmethod
    def get_step_type(cls):
        return HASHED_MESSAGE

    def write(self, out):
        super().write(out)

        out.write_decimal32(self.hash)
        out.write_decimal32(self.time)
        out.write_decimal32(self.value)


if __name__ == '__main__':
    out = DataOutputX()
    step = HashedMessageStep(hash=12345, time=67890)
    step.value = 1000  # Setting some value
    step.write(out)
    print("Written successfully. Data:", out.get_bytes())
