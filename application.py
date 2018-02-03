from PyQt5 import QtWidgets
from interface import Ui_batch_media_converter
from json import load, dump
from time import sleep
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

        self.setupUi(window, *args, **kwargs)

    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.exit_button.clicked.connect(self.exit)

    def exit(self):
        self.allow_changes(False)

        save_state(self.fetch_state())

        exit()

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
            "skip_present_files": self.skip_present_files_checkbox.checkState()
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

        self.skip_present_files_checkbox.setChecked(kwargs.get("skip_present_files"))

    def allow_changes(self, state):
        self.input_directory_edit.setEnabled(state)
        self.output_directory_edit.setEnabled(state)

        self.input_directory_picker.setEnabled(state)
        self.output_directory_picker.setEnabled(state)

        self.input_format_combo.setEnabled(state)
        self.output_format_combo.setEnabled(state)

        self.skip_present_files_checkbox.setEnabled(state)
        self.exit_button.setEnabled(state) 

    def set_active(self, state):
        self.allow_changes(not state)

        self.start_button.setEnabled(not state)
        self.cancel_button.setEnabled(state)


if __name__ == "__main__":
    interface = Interface()
    interface.window.show()

    try:
        state = load_state()
        interface.set_state(**state)
    except FileNotFoundError:
        interface.push_status("No save state file. Is this the first run?")

    interface.push_status("Ready!", 5000)

    interface.start_button.clicked.connect(lambda: interface.set_active(True))
    interface.cancel_button.clicked.connect(lambda: interface.set_active(False))

    sys.exit(interface.app.exec_())

