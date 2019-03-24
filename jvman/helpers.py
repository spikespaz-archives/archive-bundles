import itertools
import requests
import platform
import re

from PyQt5.QtCore import QThread, QProcess, QUrl
from PyQt5 import QtCore
from PyQt5.Qt import QDesktopServices
from pathlib import Path


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
        self.success = False
        self._stopped = False

    def __del__(self):
        self.wait()

    def __call__(self, url, location="./"):
        self._url = url
        self._location = location

        self.start()

    def stop(self):
        self._stopped = True
        self.success = False
        self.endDownload.emit(str(self.file_location))
        self.exit(0)

    def run(self):
        self._stopped = False
        self.success = False

        self.beginSendRequest.emit()
        request = requests.get(self._url, stream=True)
        self.endSendRequest.emit()

        self.filesize = int(request.headers["content-length"])
        self.filename = re.findall(r"filename=(.+)", request.headers["content-disposition"])[0]

        self.filenameFound.emit(self.filename)
        self.filesizeFound.emit(self.filesize)

        self.file_location = Path(self._location, self.filename).resolve()

        self.beginDownload.emit(str(self.file_location))

        with open(self.file_location, "wb") as file:
            downloaded_bytes = 0

            for count, chunk in enumerate(request.iter_content(chunk_size=self.chunk_size)):
                if self._stopped:
                    return
                elif not chunk:
                    continue

                file.write(chunk)
                downloaded_bytes += len(chunk)

                self.bytesChanged.emit(downloaded_bytes)
                self.chunkWritten.emit(count)

        self.success = True
        self.endDownload.emit(str(self.file_location))


def open_explorer(path):
    path = Path(path).resolve()
    system = platform.system().lower()

    print(system)

    if system == "windows":
        if path.is_dir():
            QProcess.startDetached(f'explorer.exe "{path}"')
        else:
            QProcess.startDetached(f'explorer.exe /select,"{path}"')
    elif system == "darwin":
        # QProcess.execute(
        #     "/usr/bin/osascript",
        #     '-e tell application "Finder" -e activate'
        #     + f' -e select POSIX file "{path}" -e and tell -e return',
        # )
        QProcess.startDetached(f'open -R "{path}"')
    else:
        if path.is_dir():
            QDesktopServices.openUrl(QUrl(path.as_uri()))
        else:
            QDesktopServices.openUrl(QUrl(path.parent.as_uri()))


def open_path(path):
    QDesktopServices.openUrl(QUrl(path.as_uri()))
