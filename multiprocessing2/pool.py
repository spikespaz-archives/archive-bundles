from multiprocessing import Pool

PAUSE = 3
CANCEL = 4


class Pool2(Pool):
    _unfinished = []

    def wait(self):
        """Close and join the pool."""
        self.close()
        self.join()
