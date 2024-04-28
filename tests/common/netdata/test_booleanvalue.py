import unittest

from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.datainputx import new_data_input_x
from scouterx.common.netdata.dataoutputx import new_data_output_x


class TestBooleanValue(unittest.TestCase):
    def test_boolean_value(self):
        # Setup data output
        out = new_data_output_x()

        # Write a boolean value
        bvalue = BooleanValue.new_boolean_value(True)
        bvalue.write(out)

        # Setup data input from output
        in_bytes = out.get_bytes()
        inp = new_data_input_x(in_bytes)

        # Read boolean and test
        test_value = inp.read_boolean()
        self.assertTrue(test_value, "Test error: The boolean value should be True")


if __name__ == '__main__':
    unittest.main()
