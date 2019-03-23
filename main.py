import os
import sys
import json
import utils
import platform
import patoolib

from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from models import AvailableBinariesTableModel, InstalledBinariesListModel
from widgets import CheckBoxButtonGroup
from interface import Ui_MainWindow
from adoptapi import RequestOptions
from utils import DownloaderThread
from pathlib import Path
from filedict import FileDict


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

DOWNLOADS_DIR = Path(Path.home(), "Downloads")
BINARIES_DIR = Path(Path.home(), ".jvman")
SETTINGS_FILE = Path(BINARIES_DIR, "options.json")


class AppMainWindow(Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        os.makedirs(BINARIES_DIR, exist_ok=True)

        self.settings = FileDict(
            SETTINGS_FILE,
            defaults={
                "downloads_dir": DOWNLOADS_DIR,
                "binaries_dir": BINARIES_DIR,
                "filter_options": RequestOptions(many=True),
                "installs": {},
            },
        )

        self._download_thread = DownloaderThread(chunk_size=1024)

    def setupUi(self, window, *args, **kwargs):
        super().setupUi(window, *args, **kwargs)

        self.availableBinariesTableModel = AvailableBinariesTableModel()
        self.availableBinariesTableView.setModel(self.availableBinariesTableModel)
        self.availableBinariesTableView.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )

        self.installedBinariesListModel = InstalledBinariesListModel()
        self.installedBinariesListView.setModel(self.installedBinariesListModel)

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

        if PLATFORM_ARCH == "x32":
            self.archOptionLabel.setEnabled(True)

            self.x32ArchCheckBox.setChecked(True)
            self.x32ArchCheckBox.setEnabled(False)
        elif PLATFORM_ARCH == "x64":
            self.archOptionLabel.setEnabled(True)

            self.x64ArchCheckBox.setChecked(True)
            self.x64ArchCheckBox.setEnabled(False)
            self.x32ArchCheckBox.setEnabled(True)

        self.setup_connections()

        # self.set_filter_options(self.settings["filter_options"])

    def setup_connections(self):
        def _on_current_changed(index):
            tab_name = self.mainTabWidget.tabText(index)

            if tab_name == "Installed Binaries":
                self.installedBinariesListModel.populate_model()
            elif tab_name == "Available Binaries":
                self.availableBinariesTableModel.populate_model(self.get_filter_options())

        self.mainTabWidget.currentChanged.connect(_on_current_changed)

        def _on_delete_selected_binary_clicked():
            selection = self.installedBinariesListView.selectedIndexes()

            for index in selection:
                self.installedBinariesListModel.removeRows(index.row(), 1)

        self.deleteSelectedBinaryPushButton.clicked.connect(_on_delete_selected_binary_clicked)

        def _on_rows_inserted(parent, first, last):
            for row in range(first, last + 1):
                self.availableBinariesTableView.resizeRowToContents(row)

        self.availableBinariesTableModel.rowsInserted.connect(_on_rows_inserted)
        self.availableBinariesTableModel.status_change.connect(self.statusbar.showMessage)

        def _on_filter_option_toggled():
            options = self.get_filter_options()
            self.settings["filter_options"] = options
            self.availableBinariesTableModel.populate_model(options)

        for group in [
            self.javaVerButtonGroup,
            self.releaseTypeButtonGroup,
            self.binTypeButtonGroup,
            self.vmButtonGroup,
            self.heapSizeButtonGroup,
            self.archButtonGroup,
        ]:
            group.buttonToggled.connect(_on_filter_option_toggled)

        def _on_begin_send_request():
            self.availableBinariesProgressBar.setMaximum(0)

        self._download_thread.beginSendRequest.connect(_on_begin_send_request)

        def _on_begin_download():
            self.availableBinariesProgressBar.setMaximum(self._download_thread.filesize)
            self.availableBinariesProgressBar.setFormat("Downloading... %p%")

        self._download_thread.beginDownload.connect(_on_begin_download)

        def _on_end_download():
            self.availableBinariesProgressBar.setFormat(
                f'Downloaded "{self._download_thread.filename}" successfully!'
            )

            self.availableBinariesTableView.setEnabled(True)
            self.availableBinariesDownloadButton.setEnabled(True)
            self.availableBinariesInstallButton.setEnabled(True)
            self.filterOptionsGroupBox.setEnabled(True)

            self.availableBinariesTableView.setFocus()

        self._download_thread.endDownload.connect(_on_end_download)

        self._download_thread.filesizeFound.connect(self.availableBinariesProgressBar.setMaximum)
        self._download_thread.bytesChanged.connect(self.availableBinariesProgressBar.setValue)

        self.availableBinariesInfoButton.clicked.connect(self.open_info_window)
        self.availableBinariesDownloadButton.clicked.connect(self.download_selected_binary)
        self.availableBinariesInstallButton.clicked.connect(self.install_selected_binary)

        def _on_selection_changed(selected, deselected):
            self.enable_available_binaries_tab_actions(True)
            self.availableBinariesProgressBar.setMaximum(1)
            self.availableBinariesProgressBar.setValue(0)

        self.availableBinariesTableView.selectionModel().selectionChanged.connect(
            _on_selection_changed
        )

    def open_info_window(self, *args, **kwargs):
        print("open_info_window")

    def download_selected_binary(self, *args, **kwargs):
        print("download_selected_binary")

        self.availableBinariesTableView.setEnabled(False)
        self.availableBinariesDownloadButton.setEnabled(False)
        self.availableBinariesInstallButton.setEnabled(False)
        self.filterOptionsGroupBox.setEnabled(False)

        selected_release = self.get_selected_release()
        request_url = selected_release.binaries[0].binary_link

        self._download_thread(request_url, location=self.settings["downloads_dir"])

    def install_selected_binary(self, *args, **kwargs):
        print("install_selected_binary")

        members_before = set(BINARIES_DIR.iterdir())
        print(members_before)

        def _on_end_download(filepath):
            print("_on_end_download")
            patoolib.extract_archive(filepath, outdir=self.settings["binaries_dir"])

            members_after = set(BINARIES_DIR.iterdir())

            members_delta = members_after - members_before

            if len(members_delta) == 0:
                self.statusbar.showMessage(
                    "No new JAVA_HOME directories found, possibly already installed?"
                )

                return

            print(members_delta)

            for item in members_delta:
                if item.is_dir():
                    self.register_binary_path(item, self.get_selected_release())

        self._download_thread.endDownload.connect(_on_end_download)
        self.download_selected_binary()

    def get_selected_release(self):
        selected_release = self.availableBinariesTableModel.data(
            self.availableBinariesTableView.selectedIndexes()[0],
            AvailableBinariesTableModel.ObjectRole,
        )

        return selected_release

    def enable_available_binaries_tab_actions(self, enable=True):
        self.availableBinariesInfoButton.setEnabled(True)
        self.availableBinariesDownloadButton.setEnabled(True)
        self.availableBinariesInstallButton.setEnabled(True)
        self.availableBinariesProgressBar.setEnabled(True)

    def register_binary_path(self, binary_path, selected_release):
        self.settings["installs"][binary_path.name] = selected_release

        self.statusbar.showMessage(
            f'Registered "{selected_release.binaries[0].binary_name}" as an available binary!'
        )

        self.dump_settings_file()

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


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
