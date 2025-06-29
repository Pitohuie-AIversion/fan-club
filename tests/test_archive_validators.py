import sys
import unittest
sys.path.insert(0, 'master')
from fc import archive

class ArchiveValidatorTest(unittest.TestCase):
    def test_range_validator(self):
        v = archive.make_range_validator(0, 10)
        v(5)
        with self.assertRaises(ValueError):
            v(-1)
        with self.assertRaises(ValueError):
            v(11)

    def test_length_validator(self):
        v = archive.make_length_validator(3)
        v([1, 2, 3])
        with self.assertRaises(ValueError):
            v([1, 2])

    def test_length_validator_large(self):
        """Ensure validator works for lengths beyond small integer caching."""
        v = archive.make_length_validator(300)
        v(list(range(300)))
        with self.assertRaises(ValueError):
            v(list(range(299)))

if __name__ == '__main__':
    unittest.main()
