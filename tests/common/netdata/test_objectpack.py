import unittest

from scouterx.common.netdata.datainputx import DataInputX
from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.objectpack import ObjectPack2


class TestObjectPack2(unittest.TestCase):
    def test_object_pack(self):
        obj_pack = ObjectPack2()
        obj_pack.site_id = "abdec"
        obj_pack.obj_hash = 12345
        obj_pack.obj_name = "testObjName"
        obj_pack.obj_type = "container"
        obj_pack.address = "1.1.1.1"
        obj_pack.family = 1
        obj_pack.version = "v1"
        obj_pack.wakeup = 1234565698
        obj_pack.tags.put("key1", "test")
        print(str(obj_pack))

        out = DataOutputX()
        obj_pack.write(out)
        in_ = DataInputX(out.get_bytes())
        obj_pack2 = ObjectPack2()
        obj_pack2.read(in_)
        print(str(obj_pack2))


if __name__ == '__main__':
    unittest.main()
