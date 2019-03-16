import itertools
import requests
import re

from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from os import path


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


class DownloaderThread(QThread):
    filenameFound = QtCore.pyqtSignal(str)
    filesizeFound = QtCore.pyqtSignal(int)
    bytesChanged = QtCore.pyqtSignal(int)

    def __init__(self, chunk_size=512, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chunk_size = chunk_size
        self.filename = None
        self._url = None
        self._location = None

    def __del__(self):
        self.wait()

    def __call__(self, url, location="./"):
        self._url = url
        self._location = location

        self.start()

    def run(self):
        request = requests.get(self._url)
        filesize = int(request.headers["content-length"])
        self.filename = re.findall("filename=(.+)", request.headers["content-disposition"])[0]

        self.filenameFound.emit(self.filename)
        self.filesizeFound.emit(filesize)

        with open(path.join(self._location, self.filename), "wb") as file:
            for count, chunk in enumerate(request.iter_content(chunk_size=self.chunk_size), 1):
                if not chunk:
                    continue

                file.write(chunk)

                self.bytesChanged.emit(count * self.chunk_size)
