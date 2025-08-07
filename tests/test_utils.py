"""Unit tests for the fc.utils module."""

import sys
import io
import platform
import unittest
sys.path.insert(0, 'master')
from fc import utils

class UtilsTest(unittest.TestCase):
    """Tests for platform detection and debug helpers."""
    def test_platform(self):
        result = utils.platform()
        self.assertIn(result, (utils.WINDOWS, utils.MAC, utils.LINUX, utils.UNKNOWN))
        expected = {
            'Windows': utils.WINDOWS,
            'Linux': utils.LINUX,
            'Darwin': utils.MAC
        }.get(platform.system(), utils.UNKNOWN)
        self.assertEqual(result, expected)

    def test_ln_returns_int(self):
        value = utils.ln()
        self.assertIsInstance(value, int)
        self.assertGreater(value, 0)

    def test_l_output(self):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            utils.l('msg', prefix='>', postfix='!')
        finally:
            sys.stdout = old
        out = buf.getvalue()
        self.assertTrue(out.startswith('> L:'))
        self.assertTrue(out.strip().endswith('msg!'))

if __name__ == '__main__':
    unittest.main()
