from os import devnull


class Simport:
    """
    for selftest only
    """

    def __init__(self, sentence=None):
        self.f = devnull
        self.sentence = sentence

    def isOpen(self):
        return True

    def write(self, cmd):
        with open(self.f, "w") as f:
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
        if self.sentence:
            return bytes(self.sentence, "ascii")
        else:
            return b"simulation"

    def readlines(self):
        if self.sentence:
            return [bytes(self.sentence, "ascii")]
        else:
            return [b"simulation"]

    def inWaiting(self):
        return 1024
