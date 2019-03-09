import sys
import adoptapi
import itertools

from PyQt5 import QtWidgets, QtCore
from interface import Ui_MainWindow


class AppMainWindow(Ui_MainWindow):
    def fill_available_binaries_table(self):
        versions = {
            "openjdk8": self.javaVer8CheckBox.isChecked(),
            "openjdk9": self.javaVer9CheckBox.isChecked(),
            "openjdk10": self.javaVer10CheckBox.isChecked(),
            "openjdk11": self.javaVer11CheckBox.isChecked(),
        }

        filter_options = {
            "openjdk_impl": "hotspot" if self.hotspotVmRadioButton.isChecked() else "openj9",
            "binary_type": "jre" if self.jreBinRadioButton.isChecked() else "jdk",
            "heap_size": "normal" if self.normalHeapSizeRadioButton.isChecked() else "large",
        }

        for version, checked in versions:
            if not checked:
                continue

            for release in itertools.chain(
                adoptapi.info(version, nightly=False, **filter_options),
                adoptapi.info(version, nightly=True, **filter_options),
            ):
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
