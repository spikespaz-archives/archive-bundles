#! /usr/bin/env python3
import sys
import common

from PyQt5 import QtWidgets

from interface import AdwinInterface


class AdwinApplication:
    def __init__(self, app=QtWidgets.QApplication(sys.argv), interface=AdwinInterface(QtWidgets.QMainWindow())):
        self.app = app
        self.interface = interface

    def start(self):
        self.interface.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    AdwinApplication().start()
