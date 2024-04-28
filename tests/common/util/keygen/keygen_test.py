import unittest

from scouterx.common.util.keygen.keygen import KeyGen


class TestKeyGen(unittest.TestCase):
    def test_key_gen(self):
        key_gen = KeyGen.get_instance()
        print(key_gen.next())
        print(key_gen.next())
        print(key_gen.next())
        print(key_gen.next())


if __name__ == '__main__':
    unittest.main()
