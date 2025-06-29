import sys
import queue
import unittest
sys.path.insert(0, 'master')
from fc import printer
import time

class PrinterTest(unittest.TestCase):
    def test_printer_puts_messages(self):
        q = queue.Queue()
        funcs = printer.printers(q)
        self.assertIn(printer.R, funcs)
        funcs[printer.R]('hello')
        code, msg = q.get_nowait()
        self.assertEqual(code, printer.R)
        self.assertTrue(msg.endswith('hello'))

    def test_printclient_symbol(self):
        q = queue.Queue()
        pc = printer.PrintClient(q, symbol='[TT]')
        pc.printr('hi')
        code, msg = q.get_nowait()
        self.assertEqual(code, printer.R)
        self.assertIn('[TT] ', msg)

    def test_printserver_routine(self):
        q = queue.Queue()
        class Collector(printer.PrintServer):
            def __init__(self, pq):
                super().__init__(pq)
                self.logs = []
                self.printr = lambda msg, prefix=True: self.logs.append(('r', msg))
            def print(self, code, text):
                self.logs.append((code, text))

        server = Collector(q)
        server.start()
        time.sleep(0.05)
        server.stop()
        server.thread.join(timeout=1)
        self.assertIn(('r', 'Print thread started.'), server.logs)
        self.assertIn(('r', 'Print thread terminated.'), server.logs)

if __name__ == '__main__':
    unittest.main()
