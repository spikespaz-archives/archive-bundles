from PyQt5.QtWidgets import QDialog, QTreeView, QVBoxLayout, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.Qt import QClipboard, QApplication

from .models import BinaryDetailsTreeModel


class BinaryDetailsDialog(QDialog):
    def __init__(self, data, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._data = data

        if not title:
            self.setWindowTitle(f"{self._data.binaries[0].binary_name} ({self._data.release_name})")

        self.setup_interface()

    def setup_interface(self):
        self.resize(600, 380)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.details_tree_model = BinaryDetailsTreeModel(self._data)
        self.details_tree_view = QTreeView()

        self.details_tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.details_tree_view.setAnimated(True)
        self.details_tree_view.setModel(self.details_tree_model)
        self.details_tree_view.expandAll()
        self.details_tree_view.resizeColumnToContents(0)
        self.details_tree_view.doubleClicked.connect(
            lambda index: QApplication.clipboard().setText(
                self.details_tree_model.data(index, Qt.DisplayRole)
            )
        )

        self.layout.addWidget(self.details_tree_view)
        self.setLayout(self.layout)
