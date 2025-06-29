import sys
import os
import queue
import tempfile
import unittest
sys.path.insert(0, 'master')
from fc import archive

class ArchiveCoreTest(unittest.TestCase):
    def setUp(self):
        self.q = queue.Queue()
        self.arc = archive.FCArchive(self.q, 'test', archive.FCArchive.DEFAULT)

    def test_set_and_modified(self):
        self.arc.set(archive.name, 'New Name')
        self.assertTrue(self.arc.modified())
        self.assertEqual(self.arc[archive.name], 'New Name')

    def test_add_saved_slave(self):
        slave = self.arc.DEFAULT[archive.defaultSlave]
        self.arc.add(archive.savedSlaves, slave)
        self.assertEqual(len(self.arc[archive.savedSlaves]), 1)

    def test_save_and_load(self):
        self.arc.set(archive.name, 'Saved')
        fd, path = tempfile.mkstemp()
        os.close(fd)
        try:
            self.arc.save(path)
            self.arc.set(archive.name, 'Changed')
            self.arc.load(path)
            self.assertEqual(self.arc[archive.name], 'Saved')
        finally:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
