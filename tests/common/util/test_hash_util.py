import unittest

from scouterx.common.util.hash_util import hash_string


class TestHashFunction(unittest.TestCase):
    def test_hash_string(self):
        print(f"hash value: {hash_string('hello world')}")
        print(f"hash value: {hash_string('**&^%hello world')}")


if __name__ == '__main__':
    unittest.main()
