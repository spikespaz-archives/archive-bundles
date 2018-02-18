from multiprocessing import pool
from multiprocessing import Queue


PAUSE = 3


class Pool(pool.Pool):
    def __reduce__(self):
        super().__reduce__()

    _unfinished = Queue()

    def wait(self):
        """Close and join the pool."""
        self.close()
        self.join()

    def pause(self):
        """Pause the pool by moving all unfinished processes to another queue."""
        if self._state == pool.RUN:
            while not self._taskqueue.empty():
                self._unfinished.put(self._taskqueue.get())

            self._state = PAUSE

    def resume(self):
        """Unpause, move all tasks back into the task queue and maintain the pool."""
        if self._state == PAUSE:
            while not self._unfinished.empty():
                self._taskqueue.put(self._unfinished.get())

            self._state = pool.RUN
            self._maintain_pool()

    def cancel(self):
        """Empty all queues and blocks."""
        while not self._taskqueue.empty():
            self._taskqueue.get()

        while not self._unfinished.empty():
            self._unfinished.get()

        self.wait()
