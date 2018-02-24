#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from interface import Ui_MarkerWindow
from time import time
from markdown2 import Markdown
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow


class UpdateHandler:
    def __init__(self, runner, callback):
        self.runner = runner
        self.callback = callback
        self._thread = None
        self._last_update = 0

    def _runner(self, newinput):
        output = self.runner(newinput)

        if self._last_update <= time():
            self.callback(output)

    def run(self, newinput):
        self._thread = Thread(target=self._runner(newinput), daemon=True)
        self._last_update = time()


class MarkerWindow(Ui_MarkerWindow):
    def __init__(self, app=QApplication([]), window=QMainWindow()):
        self.window = window
        self.app = app
        self.setupUi(window)

        self.extras = [
            "code-friendly", "cuddled-lists", "fenced-code-blocks", "footnotes", "header-ids",
            "markdown-in-html", "metadata", "pyshell", "smarty-pants", "target-blank-links", "toc", "tables",
            "use-file-vars", "wiki-tables", "tag-friendly"
        ]

        self.renderer = Markdown(extras=self.extras)
        self.render_handler = UpdateHandler(self.renderer.convert, self.markup_preview.setText)

        self.markup_editor.textChanged.connect(self.update_preview)

        self.markup_editor.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_editor, self.markup_preview))
        self.markup_preview.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_preview, self.markup_editor))

    def update_preview(self):
        self.render_handler.run(self.markup_editor.toPlainText())

    def sync_scroll(self, master, slave):
        if master.underMouse():
            master_scroll = master.verticalScrollBar()
            slave_scroll = slave.verticalScrollBar()
            master_maximum = master_scroll.maximum()

            if master_maximum:
                slave_scroll.setValue(slave_scroll.maximum() * (master_scroll.value() / master_maximum))

    def show(self):
        self.window.show()


if __name__ == "__main__":
    from sys import exit as sys_exit

    marker = MarkerWindow()
    marker.show()

    sys_exit(marker.app.exec_())
