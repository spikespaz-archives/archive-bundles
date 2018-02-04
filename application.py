from PyQt5 import QtWidgets
from interface import Ui_batch_media_file_converter
from json import load, dump
from time import sleep
from utils import is_path_exists, is_path_exists_or_creatable, open_directory_picker
import sys

# Constant to represent the name of the save state file
SAVE_STATE_FILE = "bmfc_state.json"


def save_state(state):
    """Save application json state to the `SAVE_STATE_FILE`."""
    with open(SAVE_STATE_FILE, "w") as save_state_file:
        dump(state, save_state_file)


def load_state():
    """Load application JSON state from `SAVE_STATE_FILE`."""
    with open(SAVE_STATE_FILE, "r") as save_state_file:
        return load(save_state_file)


class Interface(Ui_batch_media_file_converter):
    """Class wrapper around the uic-generated python interface file from Qt Designer."""
    def __init__(self, app=QtWidgets.QApplication([]), window=QtWidgets.QMainWindow(), *args, **kwargs):
        """Predefine app and window that is used to build the app around, and run the interface setup."""
        self.app = app  # Save the app and window for later
        self.window = window

        self.changes_allowed = True  # Define some read-only info
        self.is_active = False

        self.setupUi(window, *args, **kwargs)  # Call the setup

    def setupUi(self, *args, **kwargs):
        """Extended interface setup, does initial prep of Qt interface."""
        super().setupUi(*args, **kwargs)  # Call the super of this object and do the setup in the original interface

        self.input_directory_picker.clicked.connect(self.pick_input_directory)
        self.output_directory_picker.clicked.connect(self.pick_output_directory)

        self.input_directory_edit.textChanged.connect(self.update_ready)
        self.output_directory_edit.textChanged.connect(self.update_ready)

        self.input_format_combo.currentIndexChanged.connect(self.update_ready)
        self.output_format_combo.currentIndexChanged.connect(self.update_ready)

        self.exit_button.clicked.connect(self.exit)

    def exit(self):
        """Simple exit function to save state to `SAVE_STATE_FILE` and say "Exit." when the button is pushed."""
        self.allow_changes(False)

        save_state(self.fetch_state())
        self.push_status("Exit.")

        exit()  # Finally exit the application

    def pick_input_directory(self):
        """Open the file picker, get the new value, and set the `input_directory_edit box`
        (if there is a new value), then post that it knows about the change to the status."""
        input_directory_value = open_directory_picker(self.window, self.input_directory_edit.text())

        if input_directory_value:  # If the directory is not blank or not None
            self.input_directory_edit.setText(input_directory_value)
            self.push_status("Set new input directory: " + input_directory_value, 5000)

    def pick_output_directory(self):
        """Open the file picker, get the new value, and set the `output_directory_edit box`
        (if there is a new value), then post that it knows about the change to the status."""
        output_directory_value = open_directory_picker(self.window, self.output_directory_edit.text())

        if output_directory_value:  # If the directory is not blank or not None
            self.output_directory_edit.setText(output_directory_value)
            self.push_status("Set new output directory: " + output_directory_value, 5000)

    def update_ready(self):
        """Ensure that a valid path and format is selected for file inputs and outputs, and if they are,
        set the start button to enabled and return the ready status."""
        if (self.validate_input_directory() and self.validate_output_directory()
                and self.input_format_combo.currentText() and self.output_format_combo.currentText()):
            self.start_button.setEnabled(True)
            self.push_status("File paths and formats look good, ready to go!", 1000)
            return True
        else:  # Something isn't valid, say that in the log and return
            self.start_button.setEnabled(False)
            self.push_status("Not ready!", 1000)
            return False

    def validate_input_directory(self):
        """Return `True` if the value of `input_directory_edit` is a valid path that already exists."""
        return is_path_exists(self.input_directory_edit.text())

    def validate_output_directory(self):
        """Return `True` if the value of `input_directory_edit` is a valid
        path that already exists OR can be created."""
        return is_path_exists_or_creatable(self.output_directory_edit.text())

    def push_status(self, status, msecs=0):
        """Push a status to the status bar for X milliseconds and add it to the process log."""
        list_item = QtWidgets.QListWidgetItem()
        list_item.setText(status)

        # Add the message to the process log and scroll to bottom
        self.current_processes_list.addItem(list_item)
        self.current_processes_list.scrollToBottom()

        # Show it on the status bar for the time specified if any
        self.statusbar.showMessage(status, msecs)

    def fetch_state(self):
        """Fetch the state values of the interface and shove it into a dictionary and return."""
        return {  # Get all the values and return a dict of them
            "input_directory": self.input_directory_edit.text(),
            "output_directory": self.output_directory_edit.text(),
            "input_format": self.input_format_combo.currentText(),
            "output_format": self.output_format_combo.currentText(),
            "skip_present_files": self.skip_present_files_checkbox.checkState(),
            "window_size": (self.window.width(), self.window.height())
        }

    def set_state(self, **kwargs):
        """Set all the values of the interface to the given state dictionary."""
        self.input_directory_edit.setText(kwargs.get("input_directory", ""))
        self.output_directory_edit.setText(kwargs.get("output_directory", ""))

        input_combo_text = kwargs.get("input_format")
        output_combo_text = kwargs.get("output_format")

        # If anything is found in the keyword args, find the current index of the state item and set that.
        # This is used instead of just saving and setting the index because the items can move in the combo boxes.
        if input_combo_text:
            input_combo_items = [self.input_format_combo.itemText(item) for item in
                                 range(self.input_format_combo.count())]
            self.input_format_combo.setCurrentIndex(input_combo_items.index(input_combo_text))

        if output_combo_text:
            output_combo_items = [self.output_format_combo.itemText(item) for item in
                                  range(self.output_format_combo.count())]
            self.output_format_combo.setCurrentIndex(output_combo_items.index(output_combo_text))

        self.skip_present_files_checkbox.setChecked(kwargs.get("skip_present_files", 2))
        self.window.resize(*kwargs.get("window_size", (265, 419)))

    def allow_changes(self, boolean):
        """Unlock all of the state values of the interface and allow the user to change them."""
        self.changes_allowed = boolean  # Update the variable for info use

        self.input_directory_edit.setEnabled(boolean)
        self.output_directory_edit.setEnabled(boolean)

        self.input_directory_picker.setEnabled(boolean)
        self.output_directory_picker.setEnabled(boolean)

        self.input_format_combo.setEnabled(boolean)
        self.output_format_combo.setEnabled(boolean)

        self.skip_present_files_checkbox.setEnabled(boolean)
        self.exit_button.setEnabled(boolean)

    def set_active(self, boolean):
        """Sets the program state to active and disables the interface (`allow_changes(False)`)."""
        self.is_active = boolean

        self.allow_changes(not boolean)

        self.start_button.setEnabled(not boolean)
        self.cancel_button.setEnabled(boolean)


if __name__ == "__main__":  # The interface has been started through the main file
    interface = Interface()

    try:  # Try loading the previous state (found in the SAVE_STATE_FILE)
        saved_state = load_state()
        interface.set_state(**saved_state)
        interface.push_status("Loaded last saved state!")
    except (FileNotFoundError, ValueError):
        interface.push_status("No save state file. Is this the first run?")

    interface.window.show()  # Show the interface window

    interface.push_status("Ready!", 5000)

    # Temporary function to the buttons, disables and enables the interface changes
    interface.start_button.clicked.connect(lambda: interface.set_active(True))
    interface.cancel_button.clicked.connect(lambda: interface.set_active(False))

    # Close the application interface when the application is exited
    sys.exit(interface.app.exec_())
