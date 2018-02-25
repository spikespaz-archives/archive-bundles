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
            "code-friendly", "cuddled-lists", "fenced-code-blocks", "footnotes", "header-ids", "markdown-in-html",
            "metadata", "pyshell", "smarty-pants", "target-blank-links", "toc", "tables", "use-file-vars",
            "wiki-tables", "tag-friendly"
        ]

        self.bind_actions()

        self.renderer = Markdown(extras=self.extras)
        self.render_handler = UpdateHandler(self.renderer.convert, self.markup_preview.setText)

        self.markup_editor.textChanged.connect(self.update_preview)

        self.markup_editor.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_editor, self.markup_preview))
        self.markup_preview.verticalScrollBar().valueChanged.connect(
            lambda: self.sync_scroll(self.markup_preview, self.markup_editor))

    def bind_actions(self):
        # # File menu
        # self.action_new_file.triggered.connect()
        # self.action_new_window.triggered.connect()

        # self.action_open_file.triggered.connect()
        # self.action_open_recent.triggered.connect()

        # self.action_save.triggered.connect()
        # self.action_save_as.triggered.connect()

        # self.action_auto_save.toggled.connect()

        # self.action_preferences.triggered.connect()
        # self.action_close.triggered.connect()

        # # Edit menu
        # self.action_undo.triggered.connect()
        # self.action_redo.triggered.connect()
        # self.action_cut.triggered.connect()
        # self.action_copy.triggered.connect()
        # self.action_paste.triggered.connect()
        # self.action_find.triggered.connect()
        # self.action_replace.triggered.connect()

        # # Selection menu
        # self.action_select_all.triggered.connect()

        # self.action_increase_indent.triggered.connect()
        # self.action_decrease_indent.triggered.connect()

        # self.action_bold.triggered.connect()
        # self.action_italic.triggered.connect()
        # self.action_underline.triggered.connect()
        # self.action_strikethrough.triggered.connect()

        # self.action_superscript.triggered.connect()
        # self.action_subscript.triggered.connect()

        # self.action_insert_link_inline.triggered.connect()
        # self.action_insert_link_reference.triggered.connect()

        # self.action_insert_image_inline.triggered.connect()
        # self.action_insert_image_reference.toggled.connect()

        # self.action_ordered_list.triggered.connect()
        # self.action_unordered_list.triggered.connect()

        # # View menu
        # self.action_wrap_editor.toggled.connect()
        # self.action_wrap_preview.toggled.connect()

        # self.action_increase_zoom.triggered.connect()
        # self.action_decrease_zoom.triggered.connect()
        # self.action_reset_zoom.triggered.connect()

        self.action_expand_editor.triggered.connect(self.expand_markup_editor)
        self.action_expand_preview.triggered.connect(self.expand_markup_preview)

    def expand_markup_editor(self):
        self.splitter.setSizes([1, int(self.markup_editor.width() == 0)])

    def expand_markup_preview(self):
        self.splitter.setSizes([int(self.markup_preview.width() == 0), 1])

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
