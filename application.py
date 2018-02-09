#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import utilities as utils

from os import path
from PyQt5 import QtWidgets
from json import load, dump
from darkstyle import QDarkPalette
from contextlib import contextmanager
from multiprocessing import freeze_support
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
        self.active_pool = None

        self.window_theme = "custom"

        self.interface = Interface(window)

        self._bind_actions()
        self._bind_changes()

        fetched_state = self.read_state()

        if fetched_state:
            self.interface.push_console_message("Loaded options from save state file.")
        else:
            self.interface.push_console_message("Couldn't load save state data. Is this the first run?")

        self.set_state(**fetched_state)

        self.interface.push_status_message("Interface loaded.", 5000)

    def start(self):
        """Start and show the application."""
        self.window.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Lock the interface and close the application cleanly and safely."""
        self.interface.set_locked(True)

        self.interface.set_files_progress_undetermined(True)
        self.interface.set_data_progress_undetermined(True)

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
        self.interface.input_directory_edit.textChanged.connect(self.update_ready)
        self.interface.output_directory_edit.textChanged.connect(self.save_state)
        self.interface.output_directory_edit.textChanged.connect(self.update_ready)

        self.interface.input_format_combo.currentIndexChanged.connect(self.save_state)
        self.interface.input_format_combo.currentIndexChanged.connect(self.update_ready)
        self.interface.output_format_combo.currentIndexChanged.connect(self.save_state)
        self.interface.output_format_combo.currentIndexChanged.connect(self.update_ready)

        self.interface.overwrite_output_checkbox.stateChanged.connect(self.save_state)
        self.interface.thread_count_spinbox.valueChanged.connect(self.save_state)

        self.interface.start_button.clicked.connect(self.save_state)
        self.interface.exit_button.clicked.connect(self.save_state)

        self.window.resizeEvent = lambda _: self.save_state()

    def _bind_actions(self):
        """During initialization, bind specific actions to each element."""
        special_themed = utils.str_matches(self.window_theme, "custom", "fusion")

        def pick_input_directory():
            dir_name = utils.open_directory_picker(self.window, native=not special_themed, title="Select Input Directory")

            if dir_name:
                self.interface.input_directory_edit.setText(dir_name)
                self.interface.push_console_message("Set input directory: " + dir_name)

        def pick_output_directory():
            dir_name = utils.open_directory_picker(self.window, native=not special_themed, title="Select Output Directory")

            if dir_name:
                self.interface.output_directory_edit.setText(dir_name)
                self.interface.push_console_message("Set output directory: " + dir_name)

        self.interface.input_directory_picker.clicked.connect(pick_input_directory)
        self.interface.output_directory_picker.clicked.connect(pick_output_directory)

        self.interface.start_button.clicked.connect(lambda: (self.interface.set_data_progress_undetermined(True), self.set_active(True)))
        self.interface.cancel_button.clicked.connect(lambda: (self.interface.set_data_progress_undetermined(False), self.set_active(False)))

        self.interface.exit_button.clicked.connect(self.exit)

    def valid_input_directory(self):
        """Return `True` if the current input directory value is a valid path and exists."""
        return path.exists(self.interface.input_directory_edit.text())

    def valid_output_directory(self):
        """Return `True` if the current output directory is a valid path that exists or is creatable."""
        return utils.path_exists_or_creatable(self.interface.output_directory_edit.text())

    def update_ready(self):
        """Check all input fields for validity and enable or disable the start and cancel buttons."""
        if (self.valid_input_directory() and self.valid_output_directory()
                and self.interface.input_format_combo.currentText()
                and self.interface.output_format_combo.currentText()):
            self.interface.start_button.setEnabled(True)
            self.interface.push_status_message("Ready.")
            return True
        else:
            self.interface.start_button.setEnabled(False)
            self.interface.push_status_message("Not ready.")
            return False

    def set_active(self, state=True):
        """Set the application active state and enable or disable corresponding interface elements."""
        self.active = state

        self.interface.set_locked(state)

        self.interface.start_button.setEnabled(not state)
        self.interface.cancel_button.setEnabled(state)

    @contextmanager
    def active_state(self):
        """Set the interface as active so no changes can be made to values and yield the current state."""
        self.set_active(True)

        try:
            yield self.get_state()
        finally:
            self.set_active(False)


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

    def push_status_and_console_message(self, message, **kwargs):
        """Push a message to both the status bar and information console."""
        self.push_status_message(message, **kwargs)
        self.push_console_message(message, **kwargs)

    def set_files_progress_undetermined(self, state=True):
        self.files_completed_progress.setRange(0, int(not state))

    def set_data_progress_undetermined(self, state=True):
        self.data_completed_progress.setRange(0, int(not state))

    @contextmanager
    def files_progress_bar(self, maximum=0, fmt="%p% (%v / %m)"):
        """Set initial and final values for the files progress bar, and yield the `QtWidgets.QProgressBar` instance."""
        self.files_completed_progress.setMaximum(maximum)
        self.files_completed_progress.setFormat(fmt)

        try:
            yield self.files_completed_progress
        finally:
            self.files_completed_progress.format("%p%")
            self.files_completed_progress.reset()

    @contextmanager
    def data_progress_bar(self, maximum=0, fmt="%p% ({}h {}m {}s)"):
        """Set initial and final values for the data progress bar, and yield the `QtWidgets.QProgressBar` instance."""
        self.files_completed_progress.setMaximum(maximum)
        self.files_completed_progress.setFormat(fmt)

        def set_value(value):
            s = value // 100  # Get seconds, value is ms
            m, s = divmod(s, 60)  # Get m and s once s is divided out
            h, m = divmod(m, 60)  # Get h and m once m is divided out

            self.files_completed_progress.setFormat(fmt.format(h, m, s))  # Qt doesn't support the values we want to
            # display so we have to change the format every value update
            self.files_completed_progress.setValue(value)  # Set the value, in ms

        original_set_value = self.files_completed_progress.setValue  # Save the original setValue for later
        self.files_completed_progress.setValue = set_value  # Overwrite the default setValue

        try:
            yield self.files_completed_progress
        finally:
            self.files_completed_progress.setValue = original_set_value  # Revert change

            self.files_completed_progress.format("%p%")
            self.files_completed_progress.reset()


if __name__ == "__main__":
    freeze_support()

    Application().start()
