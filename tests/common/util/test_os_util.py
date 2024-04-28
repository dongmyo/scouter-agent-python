import unittest
import os

from scouterx.common.util.os_util import get_app_path, get_scouter_path


class TestOSUtil(unittest.TestCase):
    def test_get_app_path(self):
        """Test the get_app_path function."""
        p, _ = get_app_path()
        print(p)


class TestScouterDumpPath(unittest.TestCase):
    def test_get_scouter_path(self):
        """Test the get_scouter_path function and the path join for 'dump'."""
        p = get_scouter_path()
        print(p)
        print(os.path.join(p, 'dump'))


if __name__ == '__main__':
    unittest.main()
