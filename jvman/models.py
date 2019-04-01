import sys
import copy
from collections import OrderedDict

from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QAbstractItemModel,
    QSortFilterProxyModel,
    QAbstractListModel,
    QThread,
    QVariant,
    QModelIndex,
)
from PyQt5 import QtCore
from requests import HTTPError

from . import adoptapi
from .adoptapi import Release

ObjectRole = Qt.UserRole + 1


class GenericSortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        return left_data < right_data


class AvailableBinariesTableModel(QAbstractTableModel):
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
        elif role == ObjectRole:
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
    def __init__(self, datamodel=OrderedDict(), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._internal_data = datamodel

    def rowCount(self, parent=QModelIndex()):
        return len(self._internal_data.keys())

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() > self.rowCount() or index.column() > 0:
            return QVariant()

        name = tuple(self._internal_data.keys())[index.row()]
        release = tuple(self._internal_data.values())[index.row()]

        if role == Qt.DisplayRole:
            return f"{name} [{release.release_name}]"
        elif role == ObjectRole:
            return release

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
        new_data = OrderedDict(tuple(self._internal_data.items())[:row])
        new_data.update(
            [(f"Unnamed Release ({n})", Release(binaries=[{}])) for n in range(row, row + count)]
        )
        new_data.update(tuple(self._internal_data.items())[row + count :])
        self._internal_data.clear()
        self._internal_data.update(new_data)
        self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count)
        new_data = OrderedDict(tuple(self._internal_data.items())[:row])
        new_data.update(tuple(self._internal_data.items())[row + count :])
        self._internal_data.clear()
        self._internal_data.update(new_data)
        self.endRemoveRows()

    def add_release(self, name, release):
        if name in self._internal_data:
            self._internal_data[name] = release
            top_left = self.index(tuple(self._internal_data.keys()).index(name), 0)
            self.dataChanged.emit(top_left, top_left)
        else:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + 1)
            self._internal_data[name] = release
            self.endInsertRows()

    def add_releases(self, releases):
        for release in releases:
            self.add_release(release.binaries[0].binary_name, release)

    def get_release(self, name):
        return self._internal_data.get(name)

    def serialize(self):
        serialized = {}

        for key, value in self._internal_data.items():
            serialized[key] = value.serialize()

        return serialized


class TreeItem:
    def __init__(self, data, parent=None):
        self._parent_item = parent
        self._child_items = []
        self._item_data = data

    def childCount(self):
        return len(self._child_items)

    def columnCount(self):
        return len(self._item_data)

    def data(self, column):
        if len(self._item_data) > column:
            return self._item_data[column]

        return QVariant()

    def row(self):
        if self._parent_item:
            return self._parent_item._child_items.index(self)

        return 0

    def parentItem(self):
        return self._parent_item

    def appendChild(self, item):
        self._child_items.append(item)

    def child(self, row):
        return self._child_items[row]

    def parent(self):
        return self._parent_item


class ReferenceTreeModel(QAbstractItemModel):
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parentItem()

        if parent_item == self._root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.childCount()

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self._root_item.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole:
            return QVariant()

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0

        return super().flags(index)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root_item.data(section)

        return QVariant()


class SelectedBinaryDetailsTreeModel(ReferenceTreeModel):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._root_data = ["Field", "Value"]
        self._root_item = TreeItem(self._root_data)

        self.populate_model(data)

    def populate_model(self, release):
        release_item_release_name = TreeItem(["Release Name"], parent=self._root_item)
        release_item_release_link = TreeItem(["Release Link"], parent=self._root_item)
        release_item_timestamp = TreeItem(["Timestamp"], parent=self._root_item)
        release_item_release = TreeItem(["Release"], parent=self._root_item)
        release_item_binaries = TreeItem(["Binaries"], parent=self._root_item)
        release_item_download_count = TreeItem(["Download Count"], parent=self._root_item)

        for index, binary in enumerate(release.binaries):
            binary_item = TreeItem([index], parent=release_item_binaries)

            binary_item_os = TreeItem(["Operating System"], parent=binary_item)
            binary_item_architecture = TreeItem(["Architecture"], parent=binary_item)
            binary_item_binary_type = TreeItem(["Binary Type"], parent=binary_item)
            binary_item_openjdk_impl = TreeItem(["OpenJDK Implementation"], parent=binary_item)
            binary_item_binary_name = TreeItem(["Binary Name"], parent=binary_item)
            binary_item_binary_link = TreeItem(["Binary Link"], parent=binary_item)
            binary_item_binary_size = TreeItem(["Binary Size"], parent=binary_item)
            binary_item_checksum_link = TreeItem(["Checksum Link"], parent=binary_item)
            binary_item_version = TreeItem(["Version"], parent=binary_item)
            binary_item_version_data = TreeItem(["Version Data"], parent=binary_item)
            binary_item_version_data_openjdk_version = TreeItem(["OpenJDK Version"], parent=binary_item_version_data)
            binary_item_version_data_semver = TreeItem(["Semantic Version"], parent=binary_item_version_data)
            binary_item_version_data_optional = TreeItem(["Optional"], parent=binary_item_version_data)
            binary_item_heap_size = TreeItem(["Heap Size"], parent=binary_item)
            binary_item_download_count = TreeItem(["Download Count"], parent=binary_item)
            binary_item_updated_at = TreeItem(["Updated At"], parent=binary_item)

            binary_item.appendChild(binary_item_os)
            binary_item.appendChild(binary_item_architecture)
            binary_item.appendChild(binary_item_binary_type)
            binary_item.appendChild(binary_item_openjdk_impl)
            binary_item.appendChild(binary_item_binary_name)
            binary_item.appendChild(binary_item_binary_link)
            binary_item.appendChild(binary_item_binary_size)
            binary_item.appendChild(binary_item_checksum_link)
            binary_item.appendChild(binary_item_version)
            binary_item.appendChild(binary_item_version_data)
            binary_item_version_data.appendChild(binary_item_version_data_openjdk_version)
            binary_item_version_data.appendChild(binary_item_version_data_semver)
            binary_item_version_data.appendChild(binary_item_version_data_optional)
            binary_item.appendChild(binary_item_heap_size)
            binary_item.appendChild(binary_item_download_count)
            binary_item.appendChild(binary_item_updated_at)

            release_item_binaries.appendChild(binary_item)

        self._root_item.appendChild(release_item_release_name)
        self._root_item.appendChild(release_item_release_link)
        self._root_item.appendChild(release_item_timestamp)
        self._root_item.appendChild(release_item_release)
        self._root_item.appendChild(release_item_binaries)
        self._root_item.appendChild(release_item_download_count)
