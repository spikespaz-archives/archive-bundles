import itertools

from PyQt5.QtCore import QThread


def wrap_throwable(func, *exc):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc:
            return None

    return wrapper


def product_dicts(**kwargs):
    keys = kwargs.keys()
    values = kwargs.values()

    for instance in itertools.product(*values):
        yield dict(zip(keys, instance))


class BackgroundThread(QThread):
    def __init__(self, destination, *args, **kwargs):
        super().__init__(*args, **kwargs)

        destination.append(self)

    def __call__(self, function):
        self._target = function

        def wrapper(*args, **kwargs):
            self._args = args
            self._kwargs = kwargs

            self.start()

        return wrapper

    def __del__(self):
        self.wait()

    def run(self):
        self._target(*self._args, **self._kwargs)
