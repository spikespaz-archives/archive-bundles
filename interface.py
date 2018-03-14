#! /usr/bin/env python3
from PyQt5 import QtGui
from _interface import Ui_AdwinWindow

DISABLED = 0
UPDATE = 1
ENABLED = 2


class AdwinInterface(Ui_AdwinWindow):
    def __init__(self, window):
        self.window = window
        self.setupUi(window)
        self.set_status(DISABLED)

    def set_status(self, status=DISABLED):
        if status == DISABLED:
            self.button_status.setText("DISABLED")
            status_icon = QtGui.QIcon("icons/disabled.svg")
        if status == UPDATE:
            self.button_status.setText("UPDATE")
            status_icon = QtGui.QIcon("icons/update.svg")
        if status == ENABLED:
            self.button_status.setText("ENABLED")
            status_icon = QtGui.QIcon("icons/enabled.svg")

        self.button_status.setIcon(status_icon)
