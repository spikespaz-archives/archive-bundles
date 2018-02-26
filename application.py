#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from interface import Ui_MarkerWindow
from time import time
from markdown2 import Markdown
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow

wrapper_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>{style}</style>
</head>
<body>{markup}</body>
</html>
"""


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


class MarkerApplication(QApplication):
    def __init__(self):
        super().__init__([])

        self.window = MarkerWindow(self)

    def start(self):
        from sys import exit as sys_exit

        self.window.show()
        self.window.markup_editor.setFocus()

        sys_exit(self.exec_())


class MarkerWindow(Ui_MarkerWindow):
    def __init__(self, app=QApplication([]), window=QMainWindow()):
        self.window = window
        self.app = app
        self.setupUi(window)

        self.current_zoom = 0

        self.prepare_panels()
        self.bind_actions()
        # self.bind_sync_scrolling()

        self.renderer_extras = [
            "code-friendly", "cuddled-lists", "fenced-code-blocks", "footnotes", "header-ids", "markdown-in-html",
            "metadata", "pyshell", "smarty-pants", "target-blank-links", "toc", "tables", "use-file-vars",
            "wiki-tables", "tag-friendly"
        ]

        with open("modest.css") as stylesheet:
            self.preview_style = stylesheet.read()
            # self.preview_style += "\nhtml, body { overflow: hidden; height: 100% }"

        self.renderer = Markdown(extras=self.renderer_extras)
        self.render_handler = UpdateHandler(
            self.renderer.convert,
            lambda markup: self.markup_preview.setHtml(wrapper_html.format(style=self.preview_style, markup=markup)))

        self.markup_editor.textChanged.connect(self.update_preview)

    def prepare_panels(self):
        self.markup_preview_frame.setMinimumWidth(self.markup_editor.minimumSizeHint().width())
        self.splitter.setSizes([1, 1])

    def bind_sync_scrolling(self):
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

        self.action_increase_zoom.triggered.connect(self.increase_zoom)
        self.action_decrease_zoom.triggered.connect(self.decrease_zoom)
        self.action_reset_zoom.triggered.connect(self.reset_zoom)

        self.action_expand_editor.triggered.connect(self.expand_editor)
        self.action_expand_preview.triggered.connect(self.expand_preview)

    def increase_zoom(self):
        # self.markup_editor.zoomIn()
        self.current_zoom += 0.1
        self.markup_preview.setZoomFactor(self.current_zoom)

    def decrease_zoom(self):
        # self.markup_editor.zoomOut()
        self.current_zoom -= 0.1
        self.markup_preview.setZoomFactor(self.current_zoom)

    def reset_zoom(self):
        # self.markup_editor.zoomIn(-self.current_zoom)
        self.current_zoom = 1
        self.markup_preview.setZoomFactor(1)

    def expand_editor(self):
        self.splitter.setSizes([1, int(self.markup_editor.width() == 0)])

    def expand_preview(self):
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
    MarkerApplication().start()
