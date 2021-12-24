#! /usr/bin/env python3

from multiprocessing import pool
from multiprocessing import Queue


PAUSE = 3


class Pool(pool.Pool):
    def __reduce__(self):
        super().__reduce__()

    _unfinished = Queue()
    _historical_length = 0

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

    def unfinished(self):
        """Return the count of unfinished tasks from the queue."""
        if self._state == PAUSE:
            return self._unfinished.qsize()
        else:
            return self._taskqueue.unfinished_tasks

    def finished(self):
        """Return the count of finished tasks from the queue."""
        return self._historical_length - self.unfinished()

    def imap(self, *args, **kwargs):
        super().imap(*args, **kwargs)

        self._historical_length += 1

    def imap_unordered(self, *args, **kwargs):
        super().imap_unordered(*args, **kwargs)

        self._historical_length += 1

    def apply_async(self, *args, **kwargs):
        super().apply_async(*args, **kwargs)

        self._historical_length += 1

    def _map_async(self, *args, **kwargs):
        super()._map_async(*args, **kwargs)

        self._historical_length += 1
