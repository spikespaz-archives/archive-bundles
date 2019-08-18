import platform
import shutil
import os
import re

from collections import OrderedDict
from pathlib import Path

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QModelIndex, QSize, QTimer
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QHeaderView, QMainWindow
from PyQt5.QtCore import Qt

from . import helpers
from .helpers import DownloaderThread
from .settings import SettingsFile
from .widgets import CheckBoxButtonGroup
from .views import BinaryDetailsDialog
from .adoptapi import RequestOptions, Release
from .models import (
    AvailableBinariesTableModel,
    InstalledBinariesListModel,
    GenericSortFilterProxyModel,
    BinaryDetailsTreeModel,
    QT_OBJECTROLE,
)

# Constant to tell what the current system platform is, replacing "darwin" with "mac"
# for compatibility with the AdoptOpenJDK API.
PLATFORM_OS = (lambda x: {"darwin": "mac"}.get(x, x))(platform.system().lower())
# Constant to find the architecture of the current system, with necessary replacements
# for equivalent architectures for compatibility with the AdoptOpenJDK API.
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

DATA_SIZES = {
    "1 KiB": 1 * 2 ** 10,
    "4 KiB": 4 * 2 ** 10,
    "10 KiB": 10 * 2 ** 10,
    "100 KiB": 100 * 2 ** 10,
    "1 MiB": 1 * 2 ** 20,
    "10 MiB": 10 * 2 ** 20,
}

# Instantiate an object for serializing and deserializing the application's data in a JSON file.
SETTINGS = SettingsFile(
    Path(Path.home(), ".jvt", "settings.json"),
    # Anonymous functions that are responsible for making values serializble.
    serialize_map={
        "window_size": lambda x: (x.width(), x.height()),
        "profile_path": lambda x: str(Path.resolve(x)),
        "download_path": lambda x: str(Path.resolve(x)),
        "binaries_path": lambda x: str(Path.resolve(x)),
        "default_shell": lambda x: str(Path.resolve(x)),
        "filter_options": lambda x: x.__dict__,
        "installed_binaries": lambda x: dict(
            [(key, value.serialize()) for key, value in x.items()]
        ),
    },
    # Anonymous functions that are responsible for deserializing values.
    deserialize_map={
        "window_size": lambda x: QSize(*x),
        "profile_path": Path,
        "download_path": Path,
        "binaries_path": Path,
        "default_shell": Path,
        "filter_options": lambda x: RequestOptions(many=True, **x),
        "installed_binaries": lambda x: OrderedDict(
            [(key, Release(**value)) for key, value in x.items()]
        ),
    },
    # Default keys and values to create if they aren't already in the file on load.
    defaults={
        "interface_theme": "fusion fusion-dark accent-orange",
        "remember_window_size": True,
        "window_size": QSize(900, 450),
        "profile_path": Path(Path.home(), ".jvt"),
        "download_path": Path(Path.home(), ".jvt", "downloads"),
        "use_bytesio": (
            PLATFORM_OS == "windows"
            or re.match(
                r"^MemTotal:\s+(\d+)kB$",
                Path("/proc/meminfo").read_text(),
                re.MULTILINE | re.IGNORECASE,
            ).groups()[1]
        ),
        "dl_chunk_size": 4096,
        "binaries_path": Path(Path.home(), ".jvt", "bin"),
        "default_shell": Path(shutil.which("bash") or os.environ["comspec"]),
        "default_shell_args": ("-i", "--login") if shutil.which("bash") else tuple(),
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


# Subclass of Qt's main window widget for this application.
class AppMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the Qt UI file into this main window.
        uic.loadUi(Path(__file__).parent / "interface.ui", self)

        self.saveSettingsPushButton.setEnabled(True)
        self.saveSettingsPushButton.hide()

        # Load the settings data into the settings file object.
        SETTINGS.load()

        SETTINGS["download_path"].mkdir(parents=True, exist_ok=True)
        SETTINGS["binaries_path"].mkdir(parents=True, exist_ok=True)

        # Instantiate a thread in the background for downloads to be used across the application.
        self._download_thread = DownloaderThread(
            chunk_size=DATA_SIZES.get(*(SETTINGS["dl_chunk_size"],) * 2),
            use_bytesio=SETTINGS["use_bytesio"],
        )

        self._save_timer = QTimer()
        self._save_timer.setInterval(5000)

        self.setup_interface()
        self.setup_connections()

    def trigger_save(self):
        self._save_timer.start()

        # self.saveSettingsPushButton.setEnabled(True)
        self.saveSettingsPushButton.show()

    def resizeEvent(self, event):
        if event.oldSize() == QSize(-1, -1):
            return

        SETTINGS.__setitem__("window_size", event.size())

        self.trigger_save()

    # Perform any necessary interface set-up, such as creating control groups and view models.
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
        self.javaVerButtonGroup.add_buttons(
            self.javaVer8CheckBox,
            self.javaVer9CheckBox,
            self.javaVer10CheckBox,
            self.javaVer11CheckBox,
            self.javaVer12CheckBox,
        )

        self.releaseTypeButtonGroup = CheckBoxButtonGroup(self)
        self.releaseTypeButtonGroup.setObjectName("releaseTypeButtonGroup")
        self.releaseTypeButtonGroup.add_buttons(
            self.stableReleaseTypeCheckBox, self.nightlyReleaseTypeCheckBox
        )

        self.binTypeButtonGroup = CheckBoxButtonGroup(self)
        self.binTypeButtonGroup.setObjectName("binTypeButtonGroup")
        self.binTypeButtonGroup.add_buttons(self.jdkBinCheckBox, self.jreBinCheckBox)

        self.vmButtonGroup = CheckBoxButtonGroup(self)
        self.vmButtonGroup.setObjectName("vmButtonGroup")
        self.vmButtonGroup.add_buttons(self.hotspotVmCheckBox, self.openj9VmCheckBox)

        self.heapSizeButtonGroup = CheckBoxButtonGroup(self)
        self.heapSizeButtonGroup.setObjectName("heapSizeButtonGroup")
        self.heapSizeButtonGroup.add_buttons(
            self.normalHeapSizeCheckBox, self.largeHeapSizeCheckBox
        )

        self.archButtonGroup = CheckBoxButtonGroup(self)
        self.archButtonGroup.setObjectName("archButtonGroup")
        self.archButtonGroup.add_buttons(self.x64ArchCheckBox, self.x32ArchCheckBox)

        if PLATFORM_ARCH == "x32":
            self.archOptionLabel.setEnabled(True)
            self.x32ArchCheckBox.setEnabled(True)
        elif PLATFORM_ARCH == "x64":
            self.archOptionLabel.setEnabled(True)
            self.x64ArchCheckBox.setEnabled(True)
            self.x32ArchCheckBox.setEnabled(True)

        self.filter_options = SETTINGS["filter_options"]

    def bind_settings_options(self):
        self.interfaceThemeComboBox.currentTextChanged.connect(
            lambda x: SETTINGS.__setitem__("interface_theme", str(x))
        )
        self.interfaceThemeComboBox.currentTextChanged.connect(self.trigger_save)

        self.rememberSizeCheckBox.toggled.connect(
            lambda x: SETTINGS.__setitem__("remember_window_size", x)
        )
        self.rememberSizeCheckBox.toggled.connect(SETTINGS.dump)

        self.userProfileDirLineEdit.textEdited.connect(
            lambda x: SETTINGS.__setitem__("profile_path", Path(x))
        )
        self.userProfileDirLineEdit.textEdited.connect(self.trigger_save)

        self.dlDirLineEdit.textEdited.connect(
            lambda x: SETTINGS.__setitem__("download_path", Path(x))
        )
        self.dlDirLineEdit.textEdited.connect(self.trigger_save)

        self.useBytesIOCheckBox.toggled.connect(lambda x: SETTINGS.__setitem__("use_bytesio", x))
        self.useBytesIOCheckBox.toggled.connect(SETTINGS.dump)

        self.binDirLineEdit.textEdited.connect(
            lambda x: SETTINGS.__setitem__("binaries_path", Path(x))
        )
        self.binDirLineEdit.textEdited.connect(self.trigger_save)

        self.dlChunkSizeComboBox.currentTextChanged.connect(
            lambda x: SETTINGS.__setitem__("dl_chunk_size", x)
        )
        self.dlChunkSizeComboBox.lineEdit().textEdited.connect(self.trigger_save)
        self.dlChunkSizeComboBox.currentIndexChanged.connect(SETTINGS.dump)

        self.defaultShellLineEdit.textEdited.connect(
            lambda x: SETTINGS.__setitem__("default_shell", Path(x))
        )
        self.defaultShellLineEdit.textEdited.connect(self.trigger_save)

        self.defaultShellArgsLineEdit.textEdited.connect(
            lambda x: SETTINGS.__setitem__("default_shell_args", x.split())
        )
        self.defaultShellArgsLineEdit.textEdited.connect(self.trigger_save)

    def load_settings_options(self):
        self.interfaceThemeComboBox.setEditable(True)

        self.interfaceThemeComboBox.addItems(
            [None, "Windows", "Fusion", "Fusion Dark - Blue", "Fusion Dark - Augment Orange"]
        )

        self.interfaceThemeComboBox.setEditText(SETTINGS["interface_theme"])
        self.rememberSizeCheckBox.setChecked(SETTINGS["remember_window_size"])

        if SETTINGS["remember_window_size"]:
            self.resize(SETTINGS["window_size"])

        self.userProfileDirLineEdit.setText(str(SETTINGS["profile_path"]))
        self.dlDirLineEdit.setText(str(SETTINGS["download_path"]))
        self.useBytesIOCheckBox.setChecked(SETTINGS["use_bytesio"])

        self.dlChunkSizeComboBox.addItems(DATA_SIZES.keys())

        chunk_size_index = self.dlChunkSizeComboBox.findData(
            SETTINGS["dl_chunk_size"], Qt.DisplayRole
        )

        if chunk_size_index > -1:
            self.dlChunkSizeComboBox.setCurrentIndex(chunk_size_index)
        else:
            self.dlChunkSizeComboBox.setEditText(str(SETTINGS["dl_chunk_size"]))

        self.binDirLineEdit.setText(str(SETTINGS["binaries_path"]))
        self.defaultShellLineEdit.setText(str(SETTINGS["default_shell"]))
        self.defaultShellArgsLineEdit.setText(str(" ".join(SETTINGS["default_shell_args"])))

    def setup_connections(self):
        self.load_settings_options()
        self.bind_settings_options()

        @helpers.make_slot(int)
        @helpers.connect_slot(self.mainTabWidget.currentChanged)
        def _on_current_tab_changed(index):
            tab_name = self.mainTabWidget.tabText(index)

            if tab_name == "Installed Binaries":
                pass
            elif tab_name == "Available Binaries":
                if self.availableBinariesTableModel.rowCount() == 0:
                    self.availableBinariesTableModel.populate_model(self.filter_options)

        @helpers.make_slot()
        @helpers.connect_slot(self.deleteSelectedBinaryPushButton.clicked)
        def _on_delete_selected_binary_clicked():
            selection = self.installedBinariesListView.selectedIndexes()

            for index in selection:
                self.installedBinariesListModel.removeRows(index.row(), 1)

            SETTINGS.dump()

        @helpers.make_slot(QModelIndex, int, int)
        @helpers.connect_slot(self.availableBinariesTableModel.rowsInserted)
        def _on_rows_inserted(parent, first, last):
            del parent

            for row in range(first, last + 1):
                self.availableBinariesTableView.resizeRowToContents(row)

        @helpers.make_slot()
        @helpers.connect_slot(self.javaVerButtonGroup.buttonToggled)
        @helpers.connect_slot(self.releaseTypeButtonGroup.buttonToggled)
        @helpers.connect_slot(self.binTypeButtonGroup.buttonToggled)
        @helpers.connect_slot(self.vmButtonGroup.buttonToggled)
        @helpers.connect_slot(self.heapSizeButtonGroup.buttonToggled)
        @helpers.connect_slot(self.archButtonGroup.buttonToggled)
        def _on_filter_option_toggled():
            SETTINGS["filter_options"] = self.filter_options
            SETTINGS.dump()

            self.availableBinariesTableModel.populate_model(SETTINGS["filter_options"])

        @helpers.make_slot()
        @helpers.connect_slot(self._download_thread.beginSendRequest)
        def _on_begin_send_request():
            self.availableBinariesProgressBar.setMaximum(0)

        @helpers.make_slot()
        @helpers.connect_slot(self._download_thread.beginDownload)
        def _on_begin_download():
            self.availableBinariesProgressBar.setMaximum(self._download_thread.filesize)

            self.availableBinariesCancelButton.setEnabled(True)

        @helpers.make_slot(str)
        @helpers.connect_slot(self._download_thread.endDownload)
        def _on_end_download(file_location):
            file_location = Path(file_location)

            self._download_thread.wait()

            if not self._download_thread.success and file_location and file_location.exists():
                file_location.unlink()

            self.availableBinariesCancelButton.setEnabled(False)

            self.availableBinariesProgressBar.setFormat(
                f'Download "{self._download_thread.filename}" '
                + f'{"succeeded" if self._download_thread.success else "failed"}!'
            )

            self.availableBinariesTableView.setEnabled(True)
            self.availableBinariesDownloadButton.setEnabled(True)
            self.availableBinariesInstallButton.setEnabled(True)
            self.filterOptionsGroupBox.setEnabled(True)

            self.availableBinariesTableView.setFocus()

        @helpers.make_slot(QModelIndex, QModelIndex)
        @helpers.connect_slot(self.availableBinariesTableView.selectionModel().selectionChanged)
        def _on_available_binaries_selection_changed(selected, deselected):
            del selected, deselected

            self.enable_available_binaries_tab_actions(True)
            self.availableBinariesProgressBar.setMaximum(1)
            self.availableBinariesProgressBar.setValue(0)

        @helpers.make_slot(QModelIndex, QModelIndex)
        @helpers.connect_slot(self.installedBinariesListView.selectionModel().selectionChanged)
        def _on_installed_binaries_selection_changed(selected, deselected):
            del deselected

            if selected.isEmpty():
                self.selectedBinaryDetailsTreeView.setModel(None)
                return

            selected_release = self.selected_installed_release()
            release_model = BinaryDetailsTreeModel(selected_release)

            self.selectedBinaryDetailsTreeView.setModel(release_model)
            self.selectedBinaryDetailsTreeView.expandAll()
            self.selectedBinaryDetailsTreeView.resizeColumnToContents(0)

        @helpers.make_slot()
        @helpers.connect_slot(self.availableBinariesInfoButton.clicked)
        def _on_binaries_info_button_clicked():
            selected_binary = self.selected_available_release()

            self.open_info_window(selected_binary)

        @helpers.make_slot()
        @helpers.connect_slot(self.availableBinariesDownloadButton.clicked)
        def _on_binaries_download_button_clicked():
            selected_binary = self.selected_available_release()

            @helpers.make_slot(str)
            def _on_end_download(file_location):
                file_location = Path(file_location)

                if self._download_thread.success and file_location and file_location.exists():
                    helpers.open_explorer(file_location)

                self._download_thread.endDownload.disconnect(_on_end_download)

            self._download_thread.endDownload.connect(_on_end_download)

            self.download_binary(selected_binary)

        @helpers.make_slot()
        @helpers.connect_slot(self.availableBinariesInstallButton.clicked)
        def _on_binaries_install_button_clicked():
            selected_binary = self.selected_available_release()

            self.install_binary(selected_binary)

        @helpers.make_slot()
        @helpers.connect_slot(self.availableBinariesCancelButton.clicked)
        def _on_binaries_cancel_button_clicked():
            self.cancel_current_download()

        @helpers.make_slot()
        @helpers.connect_slot(self.renameSelectedBinaryPushButton.clicked)
        def _on_binary_rename_button_clicked():
            selected_index = self.installedBinariesListView.selectedIndexes()[0]

            self.installedBinariesListView.edit(selected_index)

        @helpers.make_slot()
        @helpers.connect_slot(self._download_thread.bytesChanged)
        def _on_binary_download_bytes_changed(current_bytes):
            max_kb = self._download_thread.filesize / 1000
            current_kb = current_bytes / 1000

            self.availableBinariesProgressBar.setValue(current_bytes)

            self.availableBinariesProgressBar.setFormat(
                f"Downloading... {current_kb / max_kb:.2%} ({current_kb:,.0f} / {max_kb:,.0f} kB)"
            )

        @helpers.make_slot(QModelIndex)
        @helpers.connect_slot(self.selectedBinaryDetailsTreeView.doubleClicked)
        def _copy_model_cell(index):
            QApplication.clipboard().setText(index.parent.model().data(index, Qt.DisplayRole))

        @helpers.make_slot()
        @helpers.connect_slot(self.userProfileDirToolButton.clicked)
        def _on_user_profile_dir_tool_button():
            SETTINGS["profile_path"] = helpers.pick_directory(
                self, "Select Profile Directory", start=SETTINGS["profile_path"]
            ).resolve()

            self.userProfileDirLineEdit.setText(str(SETTINGS["profile_path"]))

            SETTINGS.dump()

        @helpers.make_slot()
        @helpers.connect_slot(self.dlDirToolButton.clicked)
        def _on_dl_dir_tool_button():
            SETTINGS["download_path"] = helpers.pick_directory(
                self, "Select Download Directory", start=SETTINGS["download_path"]
            ).resolve()

            self.dlDirLineEdit.setText(str(SETTINGS["download_path"]))

            SETTINGS.dump()

        @helpers.make_slot()
        @helpers.connect_slot(self.binDirToolButton.clicked)
        def _on_bin_dir_tool_button():
            SETTINGS["binaries_path"] = helpers.pick_directory(
                self, "Select Binary Directory", start=SETTINGS["binaries_path"]
            ).resolve()

            self.binDirLineEdit.setText(str(SETTINGS["binaries_path"]))

            SETTINGS.dump()

        @helpers.make_slot()
        @helpers.connect_slot(self.defaultShellToolButton.clicked)
        def _on_default_shell_tool_button():
            SETTINGS["default_shell"] = helpers.pick_file(
                self,
                "Select Default Shell Executable",
                path=SETTINGS["default_shell"],
                types=("Windows Executable (*.exe)", "Unknown (*.*)"),
            ).resolve()

            self.defaultShellLineEdit.setText(str(SETTINGS["default_shell"]))

            SETTINGS.dump()

        @helpers.make_slot()
        @helpers.connect_slot(self._save_timer.timeout)
        def _on_save_settings_timer_timeout():
            SETTINGS.dump()

            self.statusbar.showMessage("Saved settings file.", 5000)

            # self.saveSettingsPushButton.setEnabled(False)
            self.saveSettingsPushButton.hide()
            self.saveSettingsPushButton.clearFocus()

        @helpers.make_slot()
        @helpers.connect_slot(self.saveSettingsPushButton.clicked)
        def _on_save_settings_button_clicked():
            self._save_timer.stop()

            _on_save_settings_timer_timeout()

        self.installedBinariesListModel.rowsInserted.connect(SETTINGS.dump)
        self.installedBinariesListModel.rowsMoved.connect(SETTINGS.dump)
        self.installedBinariesListModel.rowsRemoved.connect(SETTINGS.dump)
        self.installedBinariesListModel.rowsChanged.connect(SETTINGS.dump)
        self.installedBinariesListModel.status_change.connect(self.statusbar.showMessage)

        self.availableBinariesTableModel.status_change.connect(self.statusbar.showMessage)

        self._download_thread.filesizeFound.connect(self.availableBinariesProgressBar.setMaximum)

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
            del file_location

            self.installedBinariesListModel.add_release(release.release_name, release)

            self._download_thread.endDownload.disconnect(_on_end_download)

        self._download_thread.endDownload.connect(_on_end_download)

    def selected_available_release(self):
        return self.availableBinariesTableSortFilterProxyModel.data(
            self.availableBinariesTableView.selectedIndexes()[0], QT_OBJECTROLE
        )

    def selected_installed_release(self):
        return self.installedBinariesListModel.data(
            self.installedBinariesListView.selectedIndexes()[0], QT_OBJECTROLE
        )

    def enable_available_binaries_tab_actions(self, enable=True):
        self.availableBinariesInfoButton.setEnabled(enable)
        self.availableBinariesDownloadButton.setEnabled(enable)
        self.availableBinariesInstallButton.setEnabled(enable)
        self.availableBinariesProgressBar.setEnabled(enable)

    @property
    def filter_options(self):
        options = RequestOptions(many=True, os=[PLATFORM_OS])

        if self.javaVer8CheckBox.isChecked():
            options._version.append("openjdk8")

        if self.javaVer9CheckBox.isChecked():
            options._version.append("openjdk9")

        if self.javaVer10CheckBox.isChecked():
            options._version.append("openjdk10")

        if self.javaVer11CheckBox.isChecked():
            options._version.append("openjdk11")

        if self.javaVer12CheckBox.isChecked():
            options._version.append("openjdk12")

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

    @filter_options.setter
    def filter_options(self, options):
        self.javaVer8CheckBox.setChecked("openjdk8" in options._version)
        self.javaVer9CheckBox.setChecked("openjdk9" in options._version)
        self.javaVer10CheckBox.setChecked("openjdk10" in options._version)
        self.javaVer11CheckBox.setChecked("openjdk11" in options._version)
        self.javaVer11CheckBox.setChecked("openjdk12" in options._version)

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
