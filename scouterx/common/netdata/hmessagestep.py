from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.step import SingleStep, HASHED_MESSAGE


class HashedMessageStep(SingleStep):
    def __init__(self, hash, time):
        super().__init__()
        self.Hash = hash
        self.Time = time
        self.Value = 0  # Initialize Value to zero or any default

    @classmethod
    def get_step_type(cls):
        return HASHED_MESSAGE

    def write(self, out):
        # First, write the inherited SingleStep data
        err = super().write(out)
        if err:
            return err

        if err := out.write_decimal32(self.Hash):
            return err
        if err := out.write_decimal32(self.Time):
            return err
        return out.write_decimal32(self.Value)


if __name__ == '__main__':
    out = DataOutputX()
    step = HashedMessageStep(hash=12345, time=67890)
    step.Value = 1000  # Setting some value
    error = step.write(out)
    if error:
        print(f"Error occurred while writing: {error}")
    else:
        print("Written successfully. Data:", out.get_bytes())
