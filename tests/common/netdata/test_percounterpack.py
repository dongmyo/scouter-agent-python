import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.perfcounterpack import PerfCounterPack


class TestPerfCounterPack(unittest.TestCase):
    def test_perf_counter_pack1(self):
        pack = PerfCounterPack()
        pack.put("fvalue", 1.23)
        pack.put("ivalue", 123)
        pack.put("tvalue", " test value")
        pack.put("bvalue", False)
        print(pack)

    def test_perf_counter_pack2(self):
        pack = PerfCounterPack()
        pack.put("fvalue", 1.23)
        pack.put("ivalue", 123)
        pack.put("tvalue", " test value2")
        pack.put("bvalue", False)

        # Mocking DataOutputX and DataInputX functionality
        out = DataOutputX()
        pack.write(out)

        in_ = DataInputX(out.get_bytes())

        pack2 = PerfCounterPack()
        pack2.read(in_)
        print(pack2)


if __name__ == '__main__':
    unittest.main()
