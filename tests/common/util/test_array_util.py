import unittest

from scouterx.common.util.array_util import copy_array


class TestCopyArray(unittest.TestCase):
    def test_copy_array(self):
        src = [10, 20, 30, 40, 50, 60]
        target = copy_array(src, 2, 4)
        for v in target:
            print(v, end=" ")
        print()


if __name__ == '__main__':
    unittest.main()
