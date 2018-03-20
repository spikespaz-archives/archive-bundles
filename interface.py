#! /usr/bin/env python3
from PyQt5 import QtGui
from _interface import Ui_AdwinWindow
import common

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

    @property
    def sources(self):
        return common.str_to_list(self.edit_sources.toPlainText())

    @sources.setter
    def sources(self, in_list):
        self.edit_sources.setPlainText(common.list_to_str(in_list))

    @sources.deleter
    def sources(self):
        self.edit_sources.clear()

    @property
    def whitelist(self):
        return common.str_to_list(self.edit_whitelist.toPlainText())

    @whitelist.setter
    def whitelist(self, in_list):
        self.edit_whitelist.setPlainText(common.list_to_str(in_list))

    @whitelist.deleter
    def whitelist(self):
        self.edit_whitelist.clear()

    @property
    def blacklist(self):
        return common.str_to_list(self.edit_blacklist.toPlainText())

    @blacklist.setter
    def blacklist(self, in_list):
        self.edit_blacklist.setPlainText(common.list_to_str(in_list))

    @blacklist.deleter
    def blacklist(self):
        self.edit_blacklist.clear()

    @property
    def redirects(self):
        return common.str_to_list(self.edit_redirects.toPlainText())

    @redirects.setter
    def redirects(self, in_list):
        self.edit_redirects.setPlainText(common.list_to_str(in_list))

    @redirects.deleter
    def redirects(self):
        self.edit_redirects.clear()
