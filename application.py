#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from interface import Ui_MarkerWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class MarkerWindow(Ui_MarkerWindow):
    def __init__(self, app=QApplication([]), window=QMainWindow()):
        self.window = window
        self.app = app

        self.setupUi(window)

    def show(self):
        self.window.show()


if __name__ == "__main__":
    from sys import exit as sys_exit

    marker = MarkerWindow()
    marker.show()

    sys_exit(marker.app.exec_())
