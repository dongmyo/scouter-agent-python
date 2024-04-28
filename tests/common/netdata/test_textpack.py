import unittest

from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.textpack import TextPack


class TestTextPack(unittest.TestCase):
    def test_text_pack(self):
        pack = TextPack()
        pack.Xtype = "error"
        pack.Hash = 12345
        pack.Text = "testText"
        print(str(pack))

        out = DataOutputX()
        pack.write(out)


if __name__ == '__main__':
    unittest.main()
