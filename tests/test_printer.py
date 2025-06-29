import sys
import queue
import unittest
sys.path.insert(0, 'master')
from fc import printer

class PrinterTest(unittest.TestCase):
    def test_printer_puts_messages(self):
        q = queue.Queue()
        funcs = printer.printers(q)
        self.assertIn(printer.R, funcs)
        funcs[printer.R]('hello')
        code, msg = q.get_nowait()
        self.assertEqual(code, printer.R)
        self.assertTrue(msg.endswith('hello'))

if __name__ == '__main__':
    unittest.main()
