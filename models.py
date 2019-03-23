from PyQt5.QtCore import Qt, QAbstractTableModel, QAbstractListModel, QThread, QVariant, QModelIndex
from PyQt5 import QtCore
from requests import HTTPError
from adoptapi import Release

import adoptapi
import copy
import sys


class AvailableBinariesTableModel(QAbstractTableModel):
    ObjectRole = Qt.UserRole + 1
    status_change = QtCore.pyqtSignal(str, int)

    class UpdateThread(QThread):
        append_release = QtCore.pyqtSignal(Release)
        status_change = QtCore.pyqtSignal(str, int)

        def __init__(self, options, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._options = options

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
                            release = copy.copy(release)
                            release.binaries = [copy.deepcopy(binary)]
                            self.append_release.emit(release)
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
        elif role == AvailableBinariesTableModel.ObjectRole:
            return self._internal_data[index.row()]

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


class InstalledBinariesListModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._internal_data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._internal_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() > self.rowCount() or index.column() > 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return self._internal_data[index.row()]
        elif role == AvailableBinariesTableModel.ObjectRole:
            return self._internal_data[index.row()]

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return "Installed Binaries"
        else:
            return section

        return QVariant()

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + count)
        self._internal_data = (
            self._internal_data[:row] + ["" for _ in range(count)] + self._internal_data[row:]
        )
        self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count)
        self._internal_data = self._internal_data[:row] + self._internal_data[row + count :]
        self.endRemoveRows()
