#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import utils

from PyQt5 import QtWidgets
from json import load, dump
from darkstyle import QDarkPalette
from interface import Ui_batch_media_file_converter


# Constant to represent the name of the save state file
SAVE_STATE_FILE = "bmfc_state.json"


class Application:
    def __init__(self, app=QtWidgets.QApplication([]), window=QtWidgets.QMainWindow()):
        self.app = app
        self.window = window

        self.active = False
        self.window_theme = "custom"

        self.interface = Interface(window)

        self._bind_actions()
        self._bind_changes()

        self.set_state(**self.read_state())

    def exit(self):
        self.interface.set_locked(True)
        exit()

    @staticmethod
    def _read_state():
        with open(SAVE_STATE_FILE, "r") as file:
            return load(file)

    def read_state(self):
        try:
            return self._read_state()
        except (FileNotFoundError, ValueError):
            return {}

    @staticmethod
    def _save_state(**kwargs):
        with open(SAVE_STATE_FILE, "w") as file:
            return dump(kwargs, file, indent=2)

    def save_state(self):
        self._save_state(**self.get_state())

    def set_state(self, **kwargs):
        self.interface.set_state(**kwargs)

        self.window.resize(*kwargs.get("window_size", (350, 450)))

        self.set_window_theme(kwargs.get("window_theme", self.window_theme))

    def get_state(self):
        config = self.interface.get_state()

        window_size = self.window.size()

        config["window_size"] = (window_size.width(), window_size.height())
        config["window_theme"] = self.window_theme

        return config

    def set_window_theme(self, theme="custom"):
        self.window_theme = theme

        if theme != "custom":
            self.app.setStyle(theme)
        else:
            QDarkPalette().set_app(self.app)

    def _bind_changes(self):
        self.interface.input_directory_edit.textChanged.connect(self.save_state)
        self.interface.output_directory_edit.textChanged.connect(self.save_state)

        self.interface.input_format_combo.currentIndexChanged.connect(self.save_state)
        self.interface.output_format_combo.currentIndexChanged.connect(self.save_state)

        self.interface.overwrite_output_checkbox.stateChanged.connect(self.save_state)
        self.interface.thread_count_spinbox.valueChanged.connect(self.save_state)

        self.interface.start_button.clicked.connect(self.save_state)
        self.interface.exit_button.clicked.connect(self.save_state)

        self.window.resizeEvent = lambda _: self.save_state()

    def _bind_actions(self):
        self.interface.start_button.clicked.connect(lambda: self.interface.set_locked(True))
        self.interface.cancel_button.clicked.connect(lambda: self.interface.set_locked(False))

        self.interface.exit_button.clicked.connect(self.exit)


class Interface(Ui_batch_media_file_converter):
    def __init__(self, *args, **kwargs):
        self.locked = False

        self.setupUi(*args, **kwargs)

    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)

    def set_locked(self, state=True):
        self.locked = state

        self.input_directory_edit.setDisabled(state)
        self.input_directory_picker.setDisabled(state)

        self.output_directory_edit.setDisabled(state)
        self.output_directory_picker.setDisabled(state)

        self.input_format_combo.setDisabled(state)
        self.output_format_combo.setDisabled(state)

        self.overwrite_output_checkbox.setDisabled(state)

        self.thread_count_spinbox.setDisabled(state)

    def get_state(self):
        return {
            "locked": self.locked,

            "input_directory": self.input_directory_edit.text(),
            "output_directory": self.output_directory_edit.text(),

            "input_format": self.input_format_combo.currentText(),
            "output_format": self.output_format_combo.currentText(),

            "overwrite_output": self.overwrite_output_checkbox.checkState(),

            "thread_count": self.thread_count_spinbox.value()
        }

    def set_state(self, **kwargs):
        self.locked = kwargs.get("locked", False)

        self.input_directory_edit.setText(kwargs.get("input_directory", ""))
        self.output_directory_edit.setText(kwargs.get("output_directory", ""))

        utils.set_combo(self.input_format_combo, kwargs.get("input_format", "flac"))
        utils.set_combo(self.output_format_combo, kwargs.get("output_format", "mp3"))

        self.overwrite_output_checkbox.setChecked(kwargs.get("overwrite_output", False))

        self.thread_count_spinbox.setValue(kwargs.get("thread_count", 4))


if __name__ == "__main__":
    app = Application()
    app.window.show()

    sys.exit(app.app.exec_())
