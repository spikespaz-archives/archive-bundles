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
    chunkWritten = QtCore.pyqtSignal(int)
    beginSendRequest = QtCore.pyqtSignal()
    endSendRequest = QtCore.pyqtSignal()
    beginDownload = QtCore.pyqtSignal(str)
    endDownload = QtCore.pyqtSignal(str)

    def __init__(self, chunk_size=1024, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chunk_size = chunk_size
        self.filename = None
        self.filesize = None
        self._url = None
        self._location = None
        self.file_location = None

    def __del__(self):
        self.wait()

    def __call__(self, url, location="./"):
        self._url = url
        self._location = location

        self.start()

    def run(self):
        self.beginSendRequest.emit()
        request = requests.get(self._url)
        self.endSendRequest.emit()

        self.filesize = int(request.headers["content-length"])
        self.filename = re.findall(r"filename=(.+)", request.headers["content-disposition"])[0]

        self.filenameFound.emit(self.filename)
        self.filesizeFound.emit(self.filesize)

        self.file_location = path.join(self._location, self.filename)

        self.beginDownload.emit(self.file_location)

        with open(self.file_location, "wb") as file:
            for count, chunk in enumerate(request.iter_content(chunk_size=self.chunk_size)):
                if not chunk:
                    continue

                file.write(chunk)

                self.bytesChanged.emit(min(count * self.chunk_size, self.filesize))
                self.chunkWritten.emit(count)

        self.endDownload.emit(self.file_location)
