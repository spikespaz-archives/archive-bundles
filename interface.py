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
        batch_media_file_converter.resize(313, 438)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout_0.addItem(spacerItem)
        self.grid_layout_0 = QtWidgets.QGridLayout()
        self.grid_layout_0.setObjectName("grid_layout_0")
        self.input_format_label = QtWidgets.QLabel(self.centralwidget)
        self.input_format_label.setObjectName("input_format_label")
        self.grid_layout_0.addWidget(self.input_format_label, 0, 0, 1, 1)
        self.output_format_combo = QtWidgets.QComboBox(self.centralwidget)
        self.output_format_combo.setObjectName("output_format_combo")
        self.output_format_combo.addItem("")
        self.output_format_combo.addItem("")
        self.grid_layout_0.addWidget(self.output_format_combo, 1, 1, 1, 1)
        self.output_format_label = QtWidgets.QLabel(self.centralwidget)
        self.output_format_label.setObjectName("output_format_label")
        self.grid_layout_0.addWidget(self.output_format_label, 0, 1, 1, 1)
        self.input_format_combo = QtWidgets.QComboBox(self.centralwidget)
        self.input_format_combo.setObjectName("input_format_combo")
        self.input_format_combo.addItem("")
        self.input_format_combo.addItem("")
        self.grid_layout_0.addWidget(self.input_format_combo, 1, 0, 1, 1)
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")
        self.thread_count_label = QtWidgets.QLabel(self.centralwidget)
        self.thread_count_label.setObjectName("thread_count_label")
        self.horizontal_layout_1.addWidget(self.thread_count_label)
        self.thread_count_spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.thread_count_spinbox.setProperty("value", 4)
        self.thread_count_spinbox.setObjectName("thread_count_spinbox")
        self.horizontal_layout_1.addWidget(self.thread_count_spinbox)
        self.grid_layout_0.addLayout(self.horizontal_layout_1, 2, 1, 1, 1)
        self.overwrite_output_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.overwrite_output_checkbox.setObjectName("overwrite_output_checkbox")
        self.grid_layout_0.addWidget(self.overwrite_output_checkbox, 2, 0, 1, 1)
        self.vertical_layout_0.addLayout(self.grid_layout_0)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout_0.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout_0.addItem(spacerItem2)
        self.information_console_label = QtWidgets.QLabel(self.centralwidget)
        self.information_console_label.setObjectName("information_console_label")
        self.vertical_layout_0.addWidget(self.information_console_label)
        self.information_console_list = QtWidgets.QListWidget(self.centralwidget)
        self.information_console_list.setObjectName("information_console_list")
        self.vertical_layout_0.addWidget(self.information_console_list)
        self.actions_section_layout = QtWidgets.QHBoxLayout()
        self.actions_section_layout.setObjectName("actions_section_layout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_section_layout.addItem(spacerItem3)
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
        batch_media_file_converter.setWindowTitle(_translate("batch_media_file_converter", "FFbatcher GUI"))
        self.input_directory_label.setText(_translate("batch_media_file_converter", "Input Directory"))
        self.input_directory_edit.setToolTip(_translate("batch_media_file_converter", "The path of the input directory. All matching files in this folder and subfolders will be converted."))
        self.input_directory_picker.setToolTip(_translate("batch_media_file_converter", "Select the input directory to recurse from."))
        self.input_directory_picker.setText(_translate("batch_media_file_converter", "..."))
        self.output_directory_label.setText(_translate("batch_media_file_converter", "Output Directory"))
        self.output_directory_edit.setToolTip(_translate("batch_media_file_converter", "The path of the output directory. The subpaths of this will match the structure of the input directory exactly."))
        self.output_directory_picker.setToolTip(_translate("batch_media_file_converter", "Select directory to output converted files to."))
        self.output_directory_picker.setText(_translate("batch_media_file_converter", "..."))
        self.input_format_label.setText(_translate("batch_media_file_converter", "Input Format"))
        self.output_format_combo.setToolTip(_translate("batch_media_file_converter", "Select the output format to convert files to."))
        self.output_format_combo.setItemText(0, _translate("batch_media_file_converter", "MP3"))
        self.output_format_combo.setItemText(1, _translate("batch_media_file_converter", "FLAC"))
        self.output_format_label.setText(_translate("batch_media_file_converter", "Output Format"))
        self.input_format_combo.setToolTip(_translate("batch_media_file_converter", "Select the input format to match within the input path. These are the files that will be converted, the format can usually be decided by the file extension."))
        self.input_format_combo.setItemText(0, _translate("batch_media_file_converter", "MP3"))
        self.input_format_combo.setItemText(1, _translate("batch_media_file_converter", "FLAC"))
        self.thread_count_label.setText(_translate("batch_media_file_converter", "Thread Count"))
        self.thread_count_spinbox.setToolTip(_translate("batch_media_file_converter", "Set the number of threads to use, recommended is the number of processor cores you have. If you have mre than 4, increase this for greater efficiency."))
        self.overwrite_output_checkbox.setToolTip(_translate("batch_media_file_converter", "Overwrite existing output files. This can be useful if a previous operation was force quit, and you would like to overwrite several corrupted files."))
        self.overwrite_output_checkbox.setText(_translate("batch_media_file_converter", "Overwrite Output"))
        self.files_completed_label.setText(_translate("batch_media_file_converter", "Files Completed"))
        self.data_completed_label.setText(_translate("batch_media_file_converter", "Data Completed"))
        self.information_console_label.setText(_translate("batch_media_file_converter", "Information Console"))
        self.start_button.setToolTip(_translate("batch_media_file_converter", "Start the conversion operation."))
        self.start_button.setText(_translate("batch_media_file_converter", "Start"))
        self.cancel_button.setToolTip(_translate("batch_media_file_converter", "Cancel the current operation, but wait for current worker threads to finish their conversions before quitting. This is a safe exit and shouldn\'t corrupt the output files."))
        self.cancel_button.setText(_translate("batch_media_file_converter", "Cancel"))
        self.exit_button.setToolTip(_translate("batch_media_file_converter", "Cancel and exit the application."))
        self.exit_button.setText(_translate("batch_media_file_converter", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    batch_media_file_converter = QtWidgets.QMainWindow()
    ui = Ui_batch_media_file_converter()
    ui.setupUi(batch_media_file_converter)
    batch_media_file_converter.show()
    sys.exit(app.exec_())

