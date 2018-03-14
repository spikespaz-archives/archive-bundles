#! /usr/bin/env python3
import sys
import common
from themes.fusion_dark import FusionDark

from PyQt5 import QtWidgets

from interface import AdwinInterface


class AdwinApplication:
    def __init__(self, app=QtWidgets.QApplication(sys.argv), interface=AdwinInterface(QtWidgets.QMainWindow())):
        self.app = app
        self.interface = interface

        FusionDark().set_app(self.app)

    def start(self):
        self.interface.window.show()
        sys.exit(self.app.exec_())

    @property
    def sources(self):
        return common.str_to_list(self.interface.edit_sources.toPlainText())

    @sources.setter
    def sources(self, in_list):
        self.interface.edit_sources.setPlainText(common.list_to_str(in_list))

    @sources.deleter
    def sources(self):
        self.interface.edit_sources.clear()

    @property
    def whitelist(self):
        return common.str_to_list(self.interface.edit_whitelist.toPlainText())

    @whitelist.setter
    def whitelist(self, in_list):
        self.interface.edit_whitelist.setPlainText(common.list_to_str(in_list))

    @whitelist.deleter
    def whitelist(self):
        self.interface.edit_whitelist.clear()

    @property
    def blacklist(self):
        return common.str_to_list(self.interface.edit_blacklist.toPlainText())

    @blacklist.setter
    def blacklist(self, in_list):
        self.interface.edit_blacklist.setPlainText(common.list_to_str(in_list))

    @blacklist.deleter
    def blacklist(self):
        self.interface.edit_blacklist.clear()

    @property
    def redirects(self):
        return common.str_to_list(self.interface.edit_redirects.toPlainText())

    @redirects.setter
    def redirects(self, in_list):
        self.interface.edit_redirects.setPlainText(common.list_to_str(in_list))

    @redirects.deleter
    def redirects(self):
        self.interface.edit_redirects.clear()


if __name__ == "__main__":
    AdwinApplication().start()
