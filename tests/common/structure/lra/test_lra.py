import unittest

from scouterx.common.structure.lra.lra import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(max_entries=10)
        for i in range(10):
            self.cache.add(i, str(i))

    def test_cache_set_and_size(self):
        self.assertEqual(self.cache.size(), 10, "Initial size error.")

        self.cache.add(3, "3")
        self.assertEqual(self.cache.size(), 10, "Size should not change after adding existing item.")

        self.assertTrue(self.cache.contains(0), "Item '0' should be contained.")

        self.cache.add(1000, "1000")
        self.assertEqual(self.cache.size(), 10, "Size error after adding new element.")
        self.assertFalse(self.cache.contains(0), "Item '0' should have been removed.")

        self.assertTrue(self.cache.contains(1), "Item '1' should still be contained.")

        self.cache.add(1001, "1001")
        self.assertEqual(self.cache.size(), 10, "Size error after another addition.")
        self.assertFalse(self.cache.contains(1), "Item '1' should have been removed.")
        self.assertTrue(self.cache.contains(1001), "Item '1001' should be present.")
        self.assertEqual(self.cache.get(1001), "1001", "Value retrieval error for 1001.")


if __name__ == '__main__':
    unittest.main()
