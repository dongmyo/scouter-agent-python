import unittest

from scouterx.common.structure.cacheset.cacheset import CacheSet


class TestCacheSet(unittest.TestCase):
    def setUp(self):
        self.cacheSet = CacheSet(10)
        for i in range(10):
            self.cacheSet.add(str(i))

    def test_cache_set(self):
        self.assertEqual(self.cacheSet.size(), 10, "Initial size error.")

        self.cacheSet.add("3")
        self.assertEqual(self.cacheSet.size(), 10, "Size should not change after adding existing item.")

        self.assertTrue(self.cacheSet.contains("0"), "'0' should be contained.")

        self.cacheSet.add("1000")
        self.assertEqual(self.cacheSet.size(), 10, "Size error after adding new element.")
        self.assertFalse(self.cacheSet.contains("0"), "'0' should have been removed.")

        self.assertTrue(self.cacheSet.contains("1"), "'1' should still be contained.")

        self.cacheSet.add("1001")
        self.assertEqual(self.cacheSet.size(), 10, "Size error after another addition.")
        self.assertFalse(self.cacheSet.contains("1"), "'1' should have been removed.")
        self.assertTrue(self.cacheSet.contains("1001"), "'1001' should be present.")


if __name__ == '__main__':
    unittest.main()
