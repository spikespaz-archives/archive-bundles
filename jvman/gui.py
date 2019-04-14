import platform
from collections import OrderedDict

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QHeaderView, QMainWindow
from pathlib import Path

from . import helpers
from .helpers import DownloaderThread
from .settings import SettingsFile
from .widgets import CheckBoxButtonGroup
from .views import BinaryDetailsDialog
from .models import (
    AvailableBinariesTableModel,
    InstalledBinariesListModel,
    GenericSortFilterProxyModel,
    BinaryDetailsTreeModel,
    ObjectRole,
)
from .adoptapi import RequestOptions, Release

PLATFORM_OS = (lambda x: {"darwin": "mac"}.get(x, x))(platform.system().lower())
PLATFORM_ARCH = (
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


SETTINGS = SettingsFile(
    Path(Path.home(), ".jvman", "settings.json"),
    serialize_map={
        "download_path": lambda x: str(Path.resolve(x)),
        "binaries_path": lambda x: str(Path.resolve(x)),
        "filter_options": lambda x: x.__dict__,
        "installed_binaries": lambda x: dict(
            [(key, value.serialize()) for key, value in x.items()]
        ),
    },
    deserialize_map={
        "download_path": Path,
        "binaries_path": Path,
        "filter_options": lambda x: RequestOptions(many=True, **x),
        "installed_binaries": lambda x: OrderedDict(
            [(key, Release(**value)) for key, value in x.items()]
        ),
    },
    defaults={
        "download_path": Path(Path.home(), "Downloads"),
        "binaries_path": Path(Path.home(), ".jvman"),
        "filter_options": RequestOptions(
            _version=["openjdk8"],
            _nightly=[False],
            openjdk_impl=["openj9"],
            os=[PLATFORM_OS],
            arch=[PLATFORM_ARCH],
            type=["jdk", "jre"],
            heap_size=["normal"],
            many=True,
        ),
        "installed_binaries": OrderedDict(),
    },
)


@QtCore.pyqtSlot()
def dump_settings(*args, **kwargs):
    SETTINGS.dump()


class AppMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path(__file__) / ".." / "interface.ui", self)

        SETTINGS.load()

        self._download_thread = DownloaderThread(chunk_size=1024)

        self.setup_interface()
        self.setup_connections()

    def setup_interface(self):
        self.availableBinariesTableModel = AvailableBinariesTableModel()
        self.availableBinariesTableSortFilterProxyModel = GenericSortFilterProxyModel()
        self.availableBinariesTableSortFilterProxyModel.setSourceModel(
            self.availableBinariesTableModel
        )
        self.availableBinariesTableView.setModel(self.availableBinariesTableSortFilterProxyModel)
        self.availableBinariesTableView.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )

        self.installedBinariesListModel = InstalledBinariesListModel(
            datamodel=SETTINGS["installed_binaries"]
        )
        self.installedBinariesListView.setModel(self.installedBinariesListModel)

        self.javaVerButtonGroup = CheckBoxButtonGroup(self)
        self.javaVerButtonGroup.setObjectName("javaVerButtonGroup")
        self.javaVerButtonGroup.addButton(self.javaVer8CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer9CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer10CheckBox)
        self.javaVerButtonGroup.addButton(self.javaVer11CheckBox)

        self.releaseTypeButtonGroup = CheckBoxButtonGroup(self)
        self.releaseTypeButtonGroup.setObjectName("releaseTypeButtonGroup")
        self.releaseTypeButtonGroup.addButton(self.stableReleaseTypeCheckBox)
        self.releaseTypeButtonGroup.addButton(self.nightlyReleaseTypeCheckBox)

        self.binTypeButtonGroup = CheckBoxButtonGroup(self)
        self.binTypeButtonGroup.setObjectName("binTypeButtonGroup")
        self.binTypeButtonGroup.addButton(self.jdkBinCheckBox)
        self.binTypeButtonGroup.addButton(self.jreBinCheckBox)

        self.vmButtonGroup = CheckBoxButtonGroup(self)
        self.vmButtonGroup.setObjectName("vmButtonGroup")
        self.vmButtonGroup.addButton(self.hotspotVmCheckBox)
        self.vmButtonGroup.addButton(self.openj9VmCheckBox)

        self.heapSizeButtonGroup = CheckBoxButtonGroup(self)
        self.heapSizeButtonGroup.setObjectName("heapSizeButtonGroup")
        self.heapSizeButtonGroup.addButton(self.normalHeapSizeCheckBox)
        self.heapSizeButtonGroup.addButton(self.largeHeapSizeCheckBox)

        self.archButtonGroup = CheckBoxButtonGroup(self)
        self.archButtonGroup.setObjectName("archButtonGroup")
        self.archButtonGroup.addButton(self.x64ArchCheckBox)
        self.archButtonGroup.addButton(self.x32ArchCheckBox)

        if PLATFORM_ARCH == "x32":
            self.archOptionLabel.setEnabled(True)
            self.x32ArchCheckBox.setEnabled(True)
        elif PLATFORM_ARCH == "x64":
            self.archOptionLabel.setEnabled(True)
            self.x64ArchCheckBox.setEnabled(True)
            self.x32ArchCheckBox.setEnabled(True)

        self.set_filter_options(SETTINGS["filter_options"])

    def setup_connections(self):
        @QtCore.pyqtSlot(int)
        def _on_current_changed(index):
            tab_name = self.mainTabWidget.tabText(index)

            if tab_name == "Installed Binaries":
                pass
            elif tab_name == "Available Binaries":
                if self.availableBinariesTableModel.rowCount() == 0:
                    self.availableBinariesTableModel.populate_model(self.get_filter_options())

        @QtCore.pyqtSlot()
        def _on_delete_selected_binary_clicked():
            selection = self.installedBinariesListView.selectedIndexes()

            for index in selection:
                self.installedBinariesListModel.removeRows(index.row(), 1)

            SETTINGS.dump()

        @QtCore.pyqtSlot(QModelIndex, int, int)
        def _on_rows_inserted(parent, first, last):
            for row in range(first, last + 1):
                self.availableBinariesTableView.resizeRowToContents(row)

        @QtCore.pyqtSlot()
        def _on_filter_option_toggled():
            options = self.get_filter_options()
            SETTINGS["filter_options"] = options
            SETTINGS.dump()

            self.availableBinariesTableModel.populate_model(options)

        @QtCore.pyqtSlot()
        def _on_begin_send_request():
            self.availableBinariesProgressBar.setMaximum(0)

        @QtCore.pyqtSlot()
        def _on_begin_download():
            self.availableBinariesProgressBar.setMaximum(self._download_thread.filesize)
            self.availableBinariesProgressBar.setFormat("Downloading... %p%")

            self.availableBinariesCancelButton.setEnabled(True)

        @QtCore.pyqtSlot(str)
        def _on_end_download(file_location):
            file_location = Path(file_location)

            self._download_thread.wait()

            if not self._download_thread.success and file_location and file_location.exists():
                file_location.unlink()

            self.availableBinariesCancelButton.setEnabled(False)

            self.availableBinariesProgressBar.setFormat(
                f'Download "{self._download_thread.filename}"'
                + f'{"succeeded" if self._download_thread.success else "failed"}!'
            )

            self.availableBinariesTableView.setEnabled(True)
            self.availableBinariesDownloadButton.setEnabled(True)
            self.availableBinariesInstallButton.setEnabled(True)
            self.filterOptionsGroupBox.setEnabled(True)

            self.availableBinariesTableView.setFocus()

        @QtCore.pyqtSlot(QModelIndex, QModelIndex)
        def _on_available_binaries_selection_changed(selected, deselected):
            self.enable_available_binaries_tab_actions(True)
            self.availableBinariesProgressBar.setMaximum(1)
            self.availableBinariesProgressBar.setValue(0)

        @QtCore.pyqtSlot(QModelIndex, QModelIndex)
        def _on_installed_binaries_selection_changed(selected, deselected):
            if selected.isEmpty():
                self.selectedBinaryDetailsTreeView.setModel(None)
                return

            selected_release = self.selected_installed_release()
            release_model = BinaryDetailsTreeModel(selected_release)

            self.selectedBinaryDetailsTreeView.setModel(release_model)
            self.selectedBinaryDetailsTreeView.expandAll()
            self.selectedBinaryDetailsTreeView.resizeColumnToContents(0)

        @QtCore.pyqtSlot()
        def _on_binaries_info_button_clicked():
            selected_binary = self.selected_available_release()

            self.open_info_window(selected_binary)

        @QtCore.pyqtSlot()
        def _on_binaries_download_button_clicked():
            selected_binary = self.selected_available_release()

            @QtCore.pyqtSlot(str)
            def _on_end_download(file_location):
                file_location = Path(file_location)

                if self._download_thread.success and file_location and file_location.exists():
                    helpers.show_file(file_location)

                self._download_thread.endDownload.disconnect(_on_end_download)

            self._download_thread.endDownload.connect(_on_end_download)

            self.download_binary(selected_binary)

        @QtCore.pyqtSlot()
        def _on_binaries_install_button_clicked():
            selected_binary = self.selected_available_release()

            self.install_binary(selected_binary)

        @QtCore.pyqtSlot()
        def _on_binaries_cancel_button_clicked():
            self.cancel_current_download()

        self.installedBinariesListModel.rowsInserted.connect(dump_settings)
        self.installedBinariesListModel.rowsMoved.connect(dump_settings)
        self.installedBinariesListModel.rowsRemoved.connect(dump_settings)
        self.installedBinariesListModel.rowsChanged.connect(dump_settings)

        self.installedBinariesListView.selectionModel().selectionChanged.connect(
            _on_installed_binaries_selection_changed
        )

        self.mainTabWidget.currentChanged.connect(_on_current_changed)
        self.deleteSelectedBinaryPushButton.clicked.connect(_on_delete_selected_binary_clicked)
        self.availableBinariesTableModel.rowsInserted.connect(_on_rows_inserted)
        self.availableBinariesTableModel.status_change.connect(self.statusbar.showMessage)

        for group in [
            self.javaVerButtonGroup,
            self.releaseTypeButtonGroup,
            self.binTypeButtonGroup,
            self.vmButtonGroup,
            self.heapSizeButtonGroup,
            self.archButtonGroup,
        ]:
            group.buttonToggled.connect(_on_filter_option_toggled)

        self._download_thread.beginSendRequest.connect(_on_begin_send_request)
        self._download_thread.beginDownload.connect(_on_begin_download)
        self._download_thread.endDownload.connect(_on_end_download)

        self._download_thread.filesizeFound.connect(self.availableBinariesProgressBar.setMaximum)
        self._download_thread.bytesChanged.connect(self.availableBinariesProgressBar.setValue)

        self.availableBinariesInfoButton.clicked.connect(_on_binaries_info_button_clicked)
        self.availableBinariesDownloadButton.clicked.connect(_on_binaries_download_button_clicked)
        self.availableBinariesInstallButton.clicked.connect(_on_binaries_install_button_clicked)
        self.availableBinariesCancelButton.clicked.connect(_on_binaries_cancel_button_clicked)

        self.availableBinariesTableView.selectionModel().selectionChanged.connect(
            _on_available_binaries_selection_changed
        )

    def cancel_current_download(self):
        self._download_thread.stop()
        self._download_thread.wait()

    def open_info_window(self, release=None):
        if not release:
            release = self.selected_available_release()

        dialog = BinaryDetailsDialog(release, parent=self)
        dialog.show()

    def download_binary(self, release=None):
        if not release:
            release = self.selected_available_release()

        self.availableBinariesTableView.setEnabled(False)
        self.availableBinariesDownloadButton.setEnabled(False)
        self.availableBinariesInstallButton.setEnabled(False)
        self.filterOptionsGroupBox.setEnabled(False)

        request_url = release.binaries[0].binary_link

        self._download_thread(request_url, location=SETTINGS["download_path"])

    def install_binary(self, release=None):
        if not release:
            release = self.selected_available_release()

        self.download_binary(release=release)

        @QtCore.pyqtSlot(str)
        def _on_end_download(file_location):
            self.installedBinariesListModel.add_release(release.release_name, release)

            self._download_thread.endDownload.disconnect(_on_end_download)

        self._download_thread.endDownload.connect(_on_end_download)

    def selected_available_release(self):
        return self.availableBinariesTableSortFilterProxyModel.data(
            self.availableBinariesTableView.selectedIndexes()[0], ObjectRole
        )

    def selected_installed_release(self):
        return self.installedBinariesListModel.data(
            self.installedBinariesListView.selectedIndexes()[0], ObjectRole
        )

    def enable_available_binaries_tab_actions(self, enable=True):
        self.availableBinariesInfoButton.setEnabled(enable)
        self.availableBinariesDownloadButton.setEnabled(enable)
        self.availableBinariesInstallButton.setEnabled(enable)
        self.availableBinariesProgressBar.setEnabled(enable)

    def get_filter_options(self):
        options = RequestOptions(many=True, os=[PLATFORM_OS])

        if self.javaVer8CheckBox.isChecked():
            options._version.append("openjdk8")

        if self.javaVer9CheckBox.isChecked():
            options._version.append("openjdk9")

        if self.javaVer10CheckBox.isChecked():
            options._version.append("openjdk10")

        if self.javaVer11CheckBox.isChecked():
            options._version.append("openjdk11")

        if self.stableReleaseTypeCheckBox.isChecked():
            options._nightly.append(False)

        if self.nightlyReleaseTypeCheckBox.isChecked():
            options._nightly.append(True)

        if self.hotspotVmCheckBox.isChecked():
            options.openjdk_impl.append("hotspot")

        if self.openj9VmCheckBox.isChecked():
            options.openjdk_impl.append("openj9")

        if PLATFORM_ARCH == "x64":
            if self.x32ArchCheckBox.isChecked():
                options.arch.append("x32")

            if self.x64ArchCheckBox.isChecked():
                options.arch.append("x64")
        else:
            options.arch.append(PLATFORM_ARCH)

        if self.jdkBinCheckBox.isChecked():
            options.type.append("jdk")

        if self.jreBinCheckBox.isChecked():
            options.type.append("jre")

        if self.normalHeapSizeCheckBox.isChecked():
            options.heap_size.append("normal")

        if self.largeHeapSizeCheckBox.isChecked():
            options.heap_size.append("large")

        return options

    def set_filter_options(self, options):
        self.javaVer8CheckBox.setChecked("openjdk8" in options._version)
        self.javaVer9CheckBox.setChecked("openjdk9" in options._version)
        self.javaVer10CheckBox.setChecked("openjdk10" in options._version)
        self.javaVer11CheckBox.setChecked("openjdk11" in options._version)

        self.stableReleaseTypeCheckBox.setChecked(False in options._nightly)
        self.nightlyReleaseTypeCheckBox.setChecked(True in options._nightly)

        self.hotspotVmCheckBox.setChecked("hotspot" in options.openjdk_impl)
        self.openj9VmCheckBox.setChecked("openj9" in options.openjdk_impl)

        self.x32ArchCheckBox.setChecked("x32" in options.arch)
        self.x64ArchCheckBox.setChecked("x64" in options.arch)

        self.jdkBinCheckBox.setChecked("jdk" in options.type)
        self.jreBinCheckBox.setChecked("jre" in options.type)

        self.normalHeapSizeCheckBox.setChecked("normal" in options.heap_size)
        self.largeHeapSizeCheckBox.setChecked("large" in options.heap_size)

        self.javaVerButtonGroup.reset()
        self.releaseTypeButtonGroup.reset()
        self.vmButtonGroup.reset()
        self.archButtonGroup.reset()
        self.binTypeButtonGroup.reset()
        self.heapSizeButtonGroup.reset()
