import unittest

from scouterx.common.util.ip_util import ip_to_bytes


class TestIpToBytes(unittest.TestCase):
    def test_ip_to_bytes(self):
        bytes_result = ip_to_bytes("118.241.190.59")
        self.assertEqual(bytes_result, b'\x76\xf1\xbe\x3b')
        print("bytes:", bytes_result)


if __name__ == '__main__':
    unittest.main()
