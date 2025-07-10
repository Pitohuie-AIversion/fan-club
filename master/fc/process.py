import multiprocessing as mp

SENDER = 0
RECEIVER = 1
SUBJECT = 2
ARGUMENTS = 3

MESSAGE = 0
COMMAND = 1
MATRIX = 2
NETWORK = 3
SLAVES = 4

ERROR = -1
STOP = 999


def message(sender, receiver, subject, args=None):
    """Create a message tuple used by the dummy test processes."""
    if args is None:
        args = ()
    return (sender, receiver, subject, args)


class FCProcess:
    """Minimal stand‑in for the original FCProcess implementation."""

    def __init__(self, pqueue, routine=None, args=None, name="FCProcess"):
        self._routine = routine
        self._args = args or {}
        self.name = name
        self._print_queue = pqueue

        self._parent_pipes = {}
        self._child_pipes = {}
        for key in (MESSAGE, COMMAND, MATRIX, NETWORK, SLAVES):
            parent_end, child_end = mp.Pipe()
            self._parent_pipes[key] = parent_end
            self._child_pipes[key] = child_end

        self._process = None
        self._sid = id(self)

    # ------------------------------------------------------------------
    def start(self, profile=None):
        if self.isActive():
            return
        data = {
            'profile': profile,
            'sid': self._sid,
            'pipes': self._child_pipes,
            'pqueue': self._print_queue,
            'args': self._args,
        }
        self._process = mp.Process(target=self._routine, args=(data,), name=self.name)
        self._process.start()

    def stop(self):
        if not self.isActive():
            return
        self._process.terminate()
        self._process.join()
        self._process = None

    def isActive(self):
        return self._process is not None and self._process.is_alive()

    # ------------------------------------------------------------------
    def messageIn(self, msg):
        self._parent_pipes[MESSAGE].send(msg)
        if msg[SUBJECT] == STOP and self._process is not None:
            self._process.join(0.1)

    def matrixIn(self, msg):
        self._parent_pipes[MATRIX].send(msg)

    def networkIn(self, msg):
        self._parent_pipes[NETWORK].send(msg)

    def slaveListIn(self, msg):
        self._parent_pipes[SLAVES].send(msg)

    def hasMessage(self, timeout=None):
        return self._parent_pipes[MESSAGE].poll(timeout)

    def hasCommand(self, timeout=None):
        return self._parent_pipes[COMMAND].poll(timeout)

    def getMessage(self):
        return self._parent_pipes[MESSAGE].recv()

    def getCommand(self):
        return self._parent_pipes[COMMAND].recv()
