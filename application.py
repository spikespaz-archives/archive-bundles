#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import utils

from os import path
from PyQt5 import QtWidgets
from json import load, dump
from darkstyle import QDarkPalette
from interface import Ui_batch_media_file_converter


#: Name of the file to write saved interface values.
SAVE_STATE_FILE = "bmfc_state.json"


class Application:
    """Utility wrapper around all application functionality and interface control."""
    def __init__(self, app=QtWidgets.QApplication([]), window=QtWidgets.QMainWindow()):
        """Self initialize the application and interface and prepare for start."""
        self.app = app
        self.window = window

        self.active = False
        self.window_theme = "custom"

        self.interface = Interface(window)

        self._bind_actions()
        self._bind_changes()

        self.set_state(**self.read_state())

    def start(self):
        """Start and show the application."""
        self.window.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Lock the interface and close the application cleanly and safely."""
        self.interface.set_locked(True)
        exit()

    def set_window_theme(self, theme="custom"):
        """Set the window theme based on a string, defaulting to the custom dark fusion theme."""
        self.window_theme = theme

        if theme != "custom":
            self.app.setStyle(theme)
        else:
            QDarkPalette().set_app(self.app)

    @staticmethod
    def _read_state():
        """Read JSON data from the `SAVE_STATE_FILE` as dictionary."""
        with open(SAVE_STATE_FILE, "r") as file:
            return load(file)

    @staticmethod
    def _save_state(**kwargs):
        """Write a dictionary passed as arguments to the `SAVE_STATE_FILE`."""
        with open(SAVE_STATE_FILE, "w") as file:
            return dump(kwargs, file, indent=2)

    def read_state(self):
        """Protected read from the `SAVE_STATE_FILE`, swallows errors and returns an empty dictionary."""
        try:
            return self._read_state()
        except (FileNotFoundError, ValueError):
            return {}

    def save_state(self):
        """Save the current state of the application (retrieved from `self.get_state()`)."""
        self._save_state(**self.get_state())

    def set_state(self, **kwargs):
        """Set the application state by keyword arguments passed."""
        self.interface.set_state(**kwargs)

        self.window.resize(*kwargs.get("window_size", (350, 450)))

        self.set_window_theme(kwargs.get("window_theme", self.window_theme))

    def get_state(self):
        """Get the current application and interface state as a dictionary."""
        config = self.interface.get_state()

        window_size = self.window.size()

        config["window_size"] = (window_size.width(), window_size.height())
        config["window_theme"] = self.window_theme

        return config

    def _bind_changes(self):
        """During initialization, bind `self.save_state()` to each element on change."""
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
        """During initialization, bind specific actions to each element."""
        self.interface.start_button.clicked.connect(lambda: self.interface.set_locked(True))
        self.interface.cancel_button.clicked.connect(lambda: self.interface.set_locked(False))

        self.interface.exit_button.clicked.connect(self.exit)

    def valid_input_directory(self):
        """Return `True` if the current input directory value is a valid path and exists."""
        return path.exists(self.interface.input_directory_edit.text())

    def valid_output_directory(self):
        """Return `True` if the current output directory is a valid path that exists or is creatable."""
        return utils.path_exists_or_creatable(self.interface.output_directory_edit.text())


class Interface(Ui_batch_media_file_converter):
    """Interface wrapper around the pre-generated Qt interface with added utility methods and fields."""
    def __init__(self, *args, **kwargs):
        """Wrapped interface initializer around `self.setupUi()` that also sets initial field values."""
        self.locked = False

        self.setupUi(*args, **kwargs)

    def set_locked(self, state=True):
        """Enable or disable all the interface elements that classify as configuration values."""
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
        """Get the values of all configuration interface elements as a dictionary."""
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
        """Set the values of the configuration interface elements to the values specified by keyword arguments."""
        self.locked = kwargs.get("locked", False)

        self.input_directory_edit.setText(kwargs.get("input_directory", ""))
        self.output_directory_edit.setText(kwargs.get("output_directory", ""))

        utils.set_combo(self.input_format_combo, kwargs.get("input_format", "flac"))
        utils.set_combo(self.output_format_combo, kwargs.get("output_format", "mp3"))

        self.overwrite_output_checkbox.setChecked(kwargs.get("overwrite_output", False))

        self.thread_count_spinbox.setValue(kwargs.get("thread_count", 4))

    def push_status_message(self, message="", duration=0):
        """Push a status to the status bar for X milliseconds."""
        # Show it on the status bar for the time specified if any (by default infinite)
        self.statusbar.showMessage(message, duration)

    def push_console_message(self, message, force=False):
        """Push a message to the information console if there is no duplicate (or `force` is `True`)."""

        if force:  # Push regardless of any duplicate
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(message)

            self.information_console_list.addItem(list_item)
            self.information_console_list.scrollToBottom()

        else:  # Run the duplicate checking logic here so it isn't done if it isn't needed
            message_count = self.information_console_list.count()  # Get the number of messages in information console

            if message_count:
                last_message = self.information_console_list.item(message_count - 1)

                if message != last_message.text():  # Don't send a duplicate
                    self.push_console_message(message, force=True)
            else:
                self.push_console_message(message, force=True)

    def push_status_and_console_message(self, message, msecs=0, force=False):
        """Push a message to both the status bar and information console."""
        self.push_status_message(message, msecs)
        self.push_console_message(message, force)



if __name__ == "__main__":
    Application().start()
