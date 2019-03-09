import sys
import adoptapi
import itertools

from PyQt5 import QtWidgets, QtCore
from interface import Ui_MainWindow


class CheckBoxButtonGroup(QtWidgets.QButtonGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setExclusive(False)
        self.buttonToggled.connect(self.__protect_remaining)

    def addButton(self, button, *args, **kwargs):
        super().addButton(button, *args, **kwargs)

        self.__protect_remaining(button, button.isChecked())

    def __protect_remaining(self, button, checked):
        checked_buttons = self.checked_buttons()

        if checked:
            for button in checked_buttons:
                button.setEnabled(True)
        elif len(checked_buttons) == 1:
            checked_buttons[0].setEnabled(False)

    def checked_buttons(self):
        return [button for button in self.buttons() if button.isChecked()]


class AppMainWindow(Ui_MainWindow):
    def setupUi(self, window, *args, **kwargs):
        super().setupUi(window, *args, **kwargs)

        self.javaVerButtonGroup = CheckBoxButtonGroup(window)
        self.javaVerButtonGroup.setObjectName("javaVerButtonGroup")
        self.javaVerButtonGroup.addButton(self.javaVer8CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer9CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer10CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer11CheckBox)

        self.releaseTypeButtonGroup = CheckBoxButtonGroup(window)
        self.releaseTypeButtonGroup.setObjectName("releaseTypeButtonGroup")
        self.releaseTypeButtonGroup.addButton(self.stableReleaseTypeCheckBox)
        self.releaseTypeButtonGroup.addButton(self.nightlyReleaseTypeCheckBox)

        self.binTypeButtonGroup = CheckBoxButtonGroup(window)
        self.binTypeButtonGroup.setObjectName("binTypeButtonGroup")
        self.binTypeButtonGroup.addButton(self.jdkBinCheckBox)
        self.binTypeButtonGroup.addButton(self.jreBinCheckBox)

        self.vmButtonGroup = CheckBoxButtonGroup(window)
        self.vmButtonGroup.setObjectName("vmButtonGroup")
        self.vmButtonGroup.addButton(self.hotspotVmCheckBox)
        self.vmButtonGroup.addButton(self.openj9VmCheckBox)

        self.heapSizeButtonGroup = CheckBoxButtonGroup(window)
        self.heapSizeButtonGroup.setObjectName("heapSizeButtonGroup")
        self.heapSizeButtonGroup.addButton(self.normalHeapSizeCheckBox)
        self.heapSizeButtonGroup.addButton(self.largeHeapSizeCheckBox)

        self.archButtonGroup = CheckBoxButtonGroup(window)
        self.archButtonGroup.setObjectName("archButtonGroup")
        self.archButtonGroup.addButton(self.x64ArchCheckBox)
        self.archButtonGroup.addButton(self.x32ArchCheckBox)

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
