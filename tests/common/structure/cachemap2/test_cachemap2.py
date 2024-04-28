import unittest

from scouterx.common.structure.cachemap2.cachemap2 import CacheMap


class TestCacheMap(unittest.TestCase):
    def setUp(self):
        self.cacheMap = CacheMap(10)
        for i in range(10):
            self.cacheMap.add(i, str(i))

    def test_cache_set_and_size(self):
        self.assertEqual(self.cacheMap.size(), 10, "Initial size error.")

        self.cacheMap.add(3, "3")
        self.assertEqual(self.cacheMap.size(), 10, "Size should not change after adding existing key.")

        self.assertTrue(self.cacheMap.contains(0), "Item 0 should be contained.")

        self.cacheMap.add(1000, "1000")
        self.assertEqual(self.cacheMap.size(), 10, "Size error after adding new element.")
        self.assertFalse(self.cacheMap.contains(0), "Item 0 should have been removed.")

        self.assertTrue(self.cacheMap.contains(1), "Item 1 should still be contained.")

        self.cacheMap.add(1001, "1001")
        self.assertEqual(self.cacheMap.size(), 10, "Size error after another addition.")
        self.assertFalse(self.cacheMap.contains(1), "Item 1 should have been removed.")
        self.assertTrue(self.cacheMap.contains(1001), "Item 1001 should be present.")

        self.assertEqual(self.cacheMap.get(1001), "1001", "Value retrieval error for 1001.")


if __name__ == '__main__':
    unittest.main()
