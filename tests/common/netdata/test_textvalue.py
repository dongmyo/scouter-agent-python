import unittest

from scouterx.common.netdata.textvalue import TextValue


class TestTextValue(unittest.TestCase):
    def test_text_value(self):
        value = TextValue("aaaa")
        print(f"value: {value.value}")


if __name__ == '__main__':
    unittest.main()
