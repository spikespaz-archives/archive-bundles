import sys
import adoptapi
import itertools
import platform

from collections import namedtuple
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.param_os = (lambda x: {"darwin": "mac"}.get(x, x))(platform.system().lower())
        self.param_arch = (
            lambda x: {
                "amd64": "x64",
                "x86_64": "x64",
                "aarch64_be": "aarch64",
                "armv8b": "aarch64",
                "armv8l": "aarch64",
                "i386": "x32",
                "i686": "x32",
                "s390": "s390x",
            }.get(x, x)
        )(platform.machine().lower())

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

        if self.param_arch == "x32":
            self.archLabel.setEnabled(True)

            self.x32ArchCheckBox.setChecked(True)
            self.x32ArchCheckBox.setEnabled(False)
        elif self.param_arch == "x64":
            self.archLabel.setEnabled(True)

            self.x64ArchCheckBox.setChecked(True)
            self.x64ArchCheckBox.setEnabled(False)
            self.x32ArchCheckBox.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
