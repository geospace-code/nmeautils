from os import devnull

try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):
    from pathlib2 import Path

class Simport():
    """
    for selftest only
    """
    def __init__(self):
        self.f = devnull

    def isOpen(self):
        return True

    def write(self, cmd):
        with open(self.f,'w') as f:
            f.write(cmd)

    def open(self):
        pass

    def close(self):
        pass

    def flushInput(self):
        pass
    def flushOutput(self):
        pass

    def readline(self):
        return b'simulation'

    def readlines(self):
        return (b'simulation line 1',b'simulation line 2')

    def inWaiting(self):
        return 1024
