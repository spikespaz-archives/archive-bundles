from PyQt5.QtCore import Qt, QModelIndex, QVariant, QAbstractTableModel, QThread
from PyQt5.QtWidgets import QButtonGroup
from requests import HTTPError
from adoptapi import Release
from PyQt5 import QtCore

import sys
import copy
import adoptapi


class CheckBoxButtonGroup(QButtonGroup):
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


class AvailableBinariesTableModel(QAbstractTableModel):
    status_change = QtCore.pyqtSignal(str, int)

    class UpdateThread(QThread):
        append_release = QtCore.pyqtSignal(Release)
        status_change = QtCore.pyqtSignal(str, int)

        def __init__(self, options, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._options = options
            self.finished.connect(self.deleteLater)

        def __del__(self):
            self.wait()

        def run(self):
            params_iter = list(self._options.products())

            for count, params in enumerate(params_iter, 1):
                percent = int(count / len(params_iter) * 100)
                self.status_change.emit(
                    f"Sending requests... {percent}% ({count}/{len(params_iter)})", 5000
                )

                response = adoptapi.info(
                    params._version, nightly=params._nightly, **params.params()
                )

                try:
                    for release in response:
                        for binary in release.binaries:
                            standalone = copy.copy(release)
                            standalone.binaries = [copy.copy(binary)]

                            self.append_release.emit(standalone)
                except HTTPError as e:
                    print(e, file=sys.stderr)
                    continue

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._column_names = [
            "Release Name",
            "Java Version",
            "Release Type",
            "Binary Type",
            "Virtial Machine",
            "Heap Size",
            "Architecture",
        ]
        self._internal_data = []
        self._update_thread = None

    def rowCount(self, parent=QModelIndex()):
        return len(self._internal_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._column_names)

    def data(self, index, role=Qt.DisplayRole):
        if (
            not index.isValid()
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()
        ):
            return QVariant()

        if role == Qt.DisplayRole:
            release = self._internal_data[index.row()]

            if index.column() == 0:  # Release Name
                return release.release_name
            elif index.column() == 1:  # Java Version
                return release.binaries[0].version
            elif index.column() == 2:  # Release Type
                return "Release" if release.release else "Nightly"
            elif index.column() == 3:  # Binary Type
                return release.binaries[0].binary_type.upper()
            elif index.column() == 4:  # Virtual Machine
                if release.binaries[0].openjdk_impl == "hotspot":
                    return "Oracle HotSpot"
                elif release.binaries[0].openjdk_impl == "openj9":
                    return "Eclipse OpenJ9"
                else:
                    return release.openjdk_impl
            elif index.column() == 5:  # Heap Size
                return release.binaries[0].heap_size.title()
            elif index.column() == 6:  # Architecture
                return release.binaries[0].architecture

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return self._column_names[section]
        else:
            return section

        return QVariant()

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        for position in range(count):
            self._internal_data.insert(row + position, Release(binaries=[{}]))

        self.endInsertRows()

        return True

    @QtCore.pyqtSlot(Release)
    def append_release(self, release):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._internal_data.append(release)
        self.endInsertRows()

    def populate_model(self, options):
        if self._update_thread:
            self._update_thread.terminate()
            self._update_thread.wait()

        self.beginResetModel()
        self._internal_data = []
        self.endResetModel()

        self._update_thread = AvailableBinariesTableModel.UpdateThread(options)
        self._update_thread.append_release.connect(self.append_release)
        self._update_thread.status_change.connect(self.status_change)

        self._update_thread.start()
