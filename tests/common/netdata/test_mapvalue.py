import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.mapvalue import MapValue


class TestMapValue(unittest.TestCase):
    def test_map_value_1(self):
        ivalue = 123
        tvalue = "test"
        bvalue = True
        map_value = MapValue()
        map_value.put("value1", ivalue)
        map_value.put("value2", tvalue)
        map_value.put("value3", bvalue)

        self.assertEqual(ivalue, map_value.get_int64("value1"))
        self.assertEqual(tvalue, map_value.get_string("value2"))
        self.assertEqual(bvalue, map_value.get_boolean("value3"))
        print(map_value)

    def test_map_value_2(self):
        ivalue = 123
        tvalue = "test"
        bvalue = True
        map_value = MapValue()
        map_value.put("value1", ivalue)
        map_value.put("value2", tvalue)
        map_value.put("value3", bvalue)

        out = DataOutputX()
        map_value.write(out)

        in_ = DataInputX(out.get_bytes())
        map_value2 = MapValue()
        map_value2.read(in_)
        self.assertEqual(ivalue, map_value2.get_int64("value1"))
        self.assertEqual(tvalue, map_value2.get_string("value2"))
        self.assertEqual(bvalue, map_value2.get_boolean("value3"))


if __name__ == '__main__':
    unittest.main()
