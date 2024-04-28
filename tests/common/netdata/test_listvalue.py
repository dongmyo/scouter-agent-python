import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.listvalue import ListValue


class TestListValue(unittest.TestCase):
    def test_list_value_1(self):
        list_value = ListValue()
        ivalue = 100
        lvalue = 4000000
        tvalue = "test"
        list_value.add_int32(ivalue)
        list_value.add_int64(lvalue)
        list_value.add_string(tvalue)
        self.assertEqual(ivalue, list_value.get_int32(0))
        self.assertEqual(lvalue, list_value.get_int64(1))
        self.assertEqual(tvalue, list_value.get_string(2))
        print(f"list value {list_value}")

    def test_list_value_2(self):
        list_value = ListValue()
        ivalue = 100
        lvalue = 4000000
        tvalue = "test"
        list_value.add_int32(ivalue)
        list_value.add_int64(lvalue)
        list_value.add_string(tvalue)
        out = DataOutputX()
        list_value.write(out)

        in_ = DataInputX(out.get_bytes())
        list_value2 = ListValue()
        list_value2.read(in_)
        self.assertEqual(ivalue, list_value2.get_int32(0))
        self.assertEqual(lvalue, list_value2.get_int64(1))
        self.assertEqual(tvalue, list_value2.get_string(2))


if __name__ == '__main__':
    unittest.main()
