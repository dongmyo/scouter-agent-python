import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX


class TestDataOutputX(unittest.TestCase):
    def test_data_output_x(self):
        out = DataOutputX()
        out.write_int8(100)
        out.write_int8(1)
        out.write_int16(13245)
        out.write_int32(20022222)
        out.write_int64(500033333333)
        out.write_string("test string....")
        out.write_string("테스트입니다.")
        out.write_float32(12.456)
        out.write_decimal(24000000)
        out.write_decimal(35698)
        out.write_boolean(True)

        inp = DataInputX(out.get_bytes())
        self.assertEqual(self.get_first_from_tuple(inp.read_int8()), 100)
        self.assertEqual(self.get_first_from_tuple(inp.read_int8()), 1)
        self.assertEqual(self.get_first_from_tuple(inp.read_int16()), 13245)
        self.assertEqual(self.get_first_from_tuple(inp.read_int32()), 20022222)
        self.assertEqual(self.get_first_from_tuple(inp.read_int64()), 500033333333)
        self.assertEqual(self.get_first_from_tuple(inp.read_string()), "test string....")
        self.assertEqual(self.get_first_from_tuple(inp.read_string()), "테스트입니다.")
        self.assertAlmostEqual(self.get_first_from_tuple(inp.read_float32()), 12.456, places=3)
        self.assertEqual(self.get_first_from_tuple(inp.read_decimal()), 24000000)
        self.assertEqual(self.get_first_from_tuple(inp.read_decimal()), 35698)
        self.assertEqual(self.get_first_from_tuple(inp.read_boolean()), True)

    @staticmethod
    def get_first_from_tuple(t: tuple):
        return t[0]


if __name__ == '__main__':
    unittest.main()
