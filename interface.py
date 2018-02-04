# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_batch_media_file_converter(object):
    def setupUi(self, batch_media_file_converter):
        batch_media_file_converter.setObjectName("batch_media_file_converter")
        batch_media_file_converter.resize(265, 419)
        self.centralwidget = QtWidgets.QWidget(batch_media_file_converter)
        self.centralwidget.setObjectName("centralwidget")
        self.vertical_layout_0 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vertical_layout_0.setObjectName("vertical_layout_0")
        self.input_directory_label = QtWidgets.QLabel(self.centralwidget)
        self.input_directory_label.setObjectName("input_directory_label")
        self.vertical_layout_0.addWidget(self.input_directory_label)
        self.input_directory_layout = QtWidgets.QHBoxLayout()
        self.input_directory_layout.setObjectName("input_directory_layout")
        self.input_directory_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.input_directory_edit.setObjectName("input_directory_edit")
        self.input_directory_layout.addWidget(self.input_directory_edit)
        self.input_directory_picker = QtWidgets.QToolButton(self.centralwidget)
        self.input_directory_picker.setObjectName("input_directory_picker")
        self.input_directory_layout.addWidget(self.input_directory_picker)
        self.vertical_layout_0.addLayout(self.input_directory_layout)
        self.output_directory_label = QtWidgets.QLabel(self.centralwidget)
        self.output_directory_label.setObjectName("output_directory_label")
        self.vertical_layout_0.addWidget(self.output_directory_label)
        self.output_directory_layout = QtWidgets.QHBoxLayout()
        self.output_directory_layout.setObjectName("output_directory_layout")
        self.output_directory_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.output_directory_edit.setObjectName("output_directory_edit")
        self.output_directory_layout.addWidget(self.output_directory_edit)
        self.output_directory_picker = QtWidgets.QToolButton(self.centralwidget)
        self.output_directory_picker.setObjectName("output_directory_picker")
        self.output_directory_layout.addWidget(self.output_directory_picker)
        self.vertical_layout_0.addLayout(self.output_directory_layout)
        self.horizontal_layout_0 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_0.setObjectName("horizontal_layout_0")
        self.vertical_layout_1 = QtWidgets.QVBoxLayout()
        self.vertical_layout_1.setObjectName("vertical_layout_1")
        self.input_format_label = QtWidgets.QLabel(self.centralwidget)
        self.input_format_label.setObjectName("input_format_label")
        self.vertical_layout_1.addWidget(self.input_format_label)
        self.input_format_combo = QtWidgets.QComboBox(self.centralwidget)
        self.input_format_combo.setObjectName("input_format_combo")
        self.input_format_combo.addItem("")
        self.input_format_combo.addItem("")
        self.vertical_layout_1.addWidget(self.input_format_combo)
        self.horizontal_layout_0.addLayout(self.vertical_layout_1)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.output_format_label = QtWidgets.QLabel(self.centralwidget)
        self.output_format_label.setObjectName("output_format_label")
        self.vertical_layout_2.addWidget(self.output_format_label)
        self.output_format_combo = QtWidgets.QComboBox(self.centralwidget)
        self.output_format_combo.setObjectName("output_format_combo")
        self.output_format_combo.addItem("")
        self.output_format_combo.addItem("")
        self.vertical_layout_2.addWidget(self.output_format_combo)
        self.horizontal_layout_0.addLayout(self.vertical_layout_2)
        self.vertical_layout_0.addLayout(self.horizontal_layout_0)
        self.skip_present_files_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.skip_present_files_checkbox.setChecked(True)
        self.skip_present_files_checkbox.setObjectName("skip_present_files_checkbox")
        self.vertical_layout_0.addWidget(self.skip_present_files_checkbox)
        self.files_completed_label = QtWidgets.QLabel(self.centralwidget)
        self.files_completed_label.setObjectName("files_completed_label")
        self.vertical_layout_0.addWidget(self.files_completed_label)
        self.files_completed_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.files_completed_progress.setProperty("value", 0)
        self.files_completed_progress.setObjectName("files_completed_progress")
        self.vertical_layout_0.addWidget(self.files_completed_progress)
        self.data_completed_label = QtWidgets.QLabel(self.centralwidget)
        self.data_completed_label.setObjectName("data_completed_label")
        self.vertical_layout_0.addWidget(self.data_completed_label)
        self.data_completed_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.data_completed_progress.setProperty("value", 0)
        self.data_completed_progress.setObjectName("data_completed_progress")
        self.vertical_layout_0.addWidget(self.data_completed_progress)
        self.current_processes_label = QtWidgets.QLabel(self.centralwidget)
        self.current_processes_label.setObjectName("current_processes_label")
        self.vertical_layout_0.addWidget(self.current_processes_label)
        self.current_processes_list = QtWidgets.QListWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.current_processes_list.setFont(font)
        self.current_processes_list.setObjectName("current_processes_list")
        self.vertical_layout_0.addWidget(self.current_processes_list)
        self.actions_section_layout = QtWidgets.QHBoxLayout()
        self.actions_section_layout.setObjectName("actions_section_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_section_layout.addItem(spacerItem)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setEnabled(False)
        self.start_button.setObjectName("start_button")
        self.actions_section_layout.addWidget(self.start_button)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setEnabled(False)
        self.cancel_button.setObjectName("cancel_button")
        self.actions_section_layout.addWidget(self.cancel_button)
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setObjectName("exit_button")
        self.actions_section_layout.addWidget(self.exit_button)
        self.vertical_layout_0.addLayout(self.actions_section_layout)
        batch_media_file_converter.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(batch_media_file_converter)
        self.statusbar.setObjectName("statusbar")
        batch_media_file_converter.setStatusBar(self.statusbar)

        self.retranslateUi(batch_media_file_converter)
        QtCore.QMetaObject.connectSlotsByName(batch_media_file_converter)

    def retranslateUi(self, batch_media_file_converter):
        _translate = QtCore.QCoreApplication.translate
        batch_media_file_converter.setWindowTitle(_translate("batch_media_file_converter", "Batch Media File Converter"))
        self.input_directory_label.setText(_translate("batch_media_file_converter", "Input Directory"))
        self.input_directory_picker.setText(_translate("batch_media_file_converter", "..."))
        self.output_directory_label.setText(_translate("batch_media_file_converter", "Output Directory"))
        self.output_directory_picker.setText(_translate("batch_media_file_converter", "..."))
        self.input_format_label.setText(_translate("batch_media_file_converter", "Input Format"))
        self.input_format_combo.setItemText(0, _translate("batch_media_file_converter", "MP3"))
        self.input_format_combo.setItemText(1, _translate("batch_media_file_converter", "FLAC"))
        self.output_format_label.setText(_translate("batch_media_file_converter", "Output Format"))
        self.output_format_combo.setItemText(0, _translate("batch_media_file_converter", "MP3"))
        self.output_format_combo.setItemText(1, _translate("batch_media_file_converter", "FLAC"))
        self.skip_present_files_checkbox.setText(_translate("batch_media_file_converter", "Skip converted files already in output directory"))
        self.files_completed_label.setText(_translate("batch_media_file_converter", "Files Completed"))
        self.data_completed_label.setText(_translate("batch_media_file_converter", "Data Completed"))
        self.current_processes_label.setText(_translate("batch_media_file_converter", "Current Processes"))
        self.start_button.setText(_translate("batch_media_file_converter", "Start"))
        self.cancel_button.setText(_translate("batch_media_file_converter", "Cancel"))
        self.exit_button.setText(_translate("batch_media_file_converter", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    batch_media_file_converter = QtWidgets.QMainWindow()
    ui = Ui_batch_media_file_converter()
    ui.setupUi(batch_media_file_converter)
    batch_media_file_converter.show()
    sys.exit(app.exec_())

