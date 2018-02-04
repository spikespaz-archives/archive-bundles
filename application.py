from PyQt5 import QtWidgets
from interface import Ui_batch_media_converter
from json import load, dump
from time import sleep
from utils import is_path_exists, is_path_exists_or_creatable, open_directory_picker
import sys

SAVE_STATE_FILE = "bmfc_state.json"


def save_state(state):
    with open(SAVE_STATE_FILE, "w") as save_state_file:
        dump(state, save_state_file)


def load_state():
    with open(SAVE_STATE_FILE, "r") as save_state_file:
        return load(save_state_file)


class Interface(Ui_batch_media_converter):
    def __init__(self, app=QtWidgets.QApplication([]), window=QtWidgets.QMainWindow(), *args, **kwargs):
        self.app = app
        self.window = window

        self.changes_allowed = True
        self.is_active = False

        self.setupUi(window, *args, **kwargs)

    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)

        self.input_directory_picker.clicked.connect(self.pick_input_directory)
        self.output_directory_picker.clicked.connect(self.pick_output_directory)

        self.input_directory_edit.textChanged.connect(self.update_ready)
        self.output_directory_edit.textChanged.connect(self.update_ready)

        self.input_format_combo.currentIndexChanged.connect(self.update_ready)
        self.output_format_combo.currentIndexChanged.connect(self.update_ready)

        self.exit_button.clicked.connect(self.exit)

    def exit(self):
        self.allow_changes(False)

        save_state(self.fetch_state())

        exit()

    def pick_input_directory(self):
        input_directory_value = open_directory_picker(self.window, self.input_directory_edit.text())

        if input_directory_value:
            self.input_directory_edit.setText(input_directory_value)

    def pick_output_directory(self):
        output_directory_value = open_directory_picker(self.window, self.output_directory_edit.text())

        if output_directory_value:
            self.output_directory_edit.setText(output_directory_value)

    def update_ready(self):
        if (self.validate_input_directory() and self.validate_output_directory()
                and self.input_format_combo.currentText() and self.output_format_combo.currentText()):
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def validate_input_directory(self):
        print(is_path_exists(self.input_directory_edit.text()))
        return is_path_exists(self.input_directory_edit.text())

    def validate_output_directory(self):
        print(is_path_exists_or_creatable(self.output_directory_edit.text()))
        return is_path_exists_or_creatable(self.output_directory_edit.text())

    def push_status(self, status, msecs=0):
        list_item = QtWidgets.QListWidgetItem()
        list_item.setText(status)

        self.current_processes_list.addItem(list_item)
        self.current_processes_list.scrollToBottom()

        self.statusbar.showMessage(status, msecs)

    def fetch_state(self):
        return {
            "input_directory": self.input_directory_edit.text(),
            "output_directory": self.output_directory_edit.text(),
            "input_format": self.input_format_combo.currentText(),
            "output_format": self.output_format_combo.currentText(),
            "skip_present_files": self.skip_present_files_checkbox.checkState(),
            "window_size": (self.window.width(), self.window.height())
        }

    def set_state(self, **kwargs):
        self.input_directory_edit.setText(kwargs.get("input_directory", ""))
        self.output_directory_edit.setText(kwargs.get("output_directory", ""))

        input_combo_text = kwargs.get("input_format")
        output_combo_text = kwargs.get("output_format")

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
        self.changes_allowed = boolean

        self.input_directory_edit.setEnabled(boolean)
        self.output_directory_edit.setEnabled(boolean)

        self.input_directory_picker.setEnabled(boolean)
        self.output_directory_picker.setEnabled(boolean)

        self.input_format_combo.setEnabled(boolean)
        self.output_format_combo.setEnabled(boolean)

        self.skip_present_files_checkbox.setEnabled(boolean)
        self.exit_button.setEnabled(boolean)

    def set_active(self, boolean):
        self.is_active = boolean

        self.allow_changes(not boolean)

        self.start_button.setEnabled(not boolean)
        self.cancel_button.setEnabled(boolean)


if __name__ == "__main__":
    interface = Interface()

    try:
        saved_state = load_state()
        interface.set_state(**saved_state)
    except (FileNotFoundError, ValueError):
        interface.push_status("No save state file. Is this the first run?")

    interface.window.show()

    interface.push_status("Ready!", 5000)

    interface.start_button.clicked.connect(lambda: interface.set_active(True))
    interface.cancel_button.clicked.connect(lambda: interface.set_active(False))

    sys.exit(interface.app.exec_())
