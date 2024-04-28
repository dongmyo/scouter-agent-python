import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.decimalvalue import DecimalValue


class TestDecimalValue(unittest.TestCase):
    def test_decimal_value(self):
        # Create a DataOutputX instance
        out = DataOutputX()

        # Create a DecimalValue with the value 1234
        dvalue = DecimalValue(1234)

        # Write the DecimalValue to the output
        dvalue.write(out)

        # Create a DataInputX instance with the output bytes
        inp = DataInputX(out.get_bytes())

        # Read the decimal value back
        result, err = inp.read_decimal()

        # Check for errors
        self.assertIsNone(err, "Error occurred while reading decimal")

        # Assert the value read is as expected
        self.assertEqual(result, 1234, "Decimal value read does not match expected value")

        # Optional: print out the result, similar to fmt.Printf in Go
        print(f"value: {result}")


if __name__ == '__main__':
    unittest.main()
