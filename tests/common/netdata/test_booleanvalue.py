import unittest

from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX


class TestBooleanValue(unittest.TestCase):
    def test_boolean_value(self):
        # Setup data output
        out = DataOutputX()

        # Write a boolean value
        bvalue = BooleanValue.new_boolean_value(True)
        bvalue.write(out)

        # Setup data input from output
        in_bytes = out.get_bytes()
        inp = DataInputX(in_bytes)

        # Read boolean and test
        test_value = inp.read_boolean()
        self.assertTrue(test_value, "Test error: The boolean value should be True")


if __name__ == '__main__':
    unittest.main()
