#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from interface import Ui_MarkerWindow
from markdown2 import Markdown
from PyQt5.QtWidgets import QApplication, QMainWindow


class MarkerWindow(Ui_MarkerWindow):
    def __init__(self, app=QApplication([]), window=QMainWindow()):
        self.window = window
        self.app = app
        self.setupUi(window)

        self.renderer = Markdown()

        self.markup_editor.textChanged.connect(self.update_preview)

        self.markup_editor.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_editor, self.markup_preview))
        self.markup_preview.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_preview, self.markup_editor))

    def update_preview(self):
        self.markup_preview.setText(
            self.renderer.convert(self.markup_editor.toPlainText()))

    def sync_scroll(self, master, slave):
        if master.underMouse():
            master_scroll = master.verticalScrollBar()
            slave_scroll = slave.verticalScrollBar()
            master_maximum = master_scroll.maximum()

            if master_maximum:
                slave_scroll.setValue(slave_scroll.maximum() *
                                    (master_scroll.value() / master_maximum))

    def show(self):
        self.window.show()


if __name__ == "__main__":
    from sys import exit as sys_exit

    marker = MarkerWindow()
    marker.show()

    sys_exit(marker.app.exec_())
