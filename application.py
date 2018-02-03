from PyQt5 import QtWidgets
from interface import Ui_batch_media_converter
from json import load, dump
import sys


SAVE_STATE_FILE = "bmfc_state.json"


class Interface(Ui_batch_media_converter):
    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.exit_button.clicked.connect(exit)

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

        input_combo_items = [self.input_format_combo.itemText(item) for item in range(self.input_format_combo.count())]
        output_combo_items = [self.output_format_combo.itemText(item) for item in range(self.output_format_combo.count())]

        self.input_format_combo.setCurrentIndex(input_combo_items.index(kwargs.get("input_format")))
        self.output_format_combo.setCurrentIndex(output_combo_items.index(kwargs.get("output_format")))

        self.skip_present_files_checkbox.setChecked(kwargs.get("skip_present_files"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    interface = Interface()
    interface.setupUi(main_window)
    main_window.show()

    try:
        with open(SAVE_STATE_FILE, "r") as save_state_file:
            save_state = load(save_state_file)
            interface.set_state(**save_state)
    except FileNotFoundError:
        interface.push_status("No save state file. Is this the first run?", 5000)

    sys.exit(app.exec_())

