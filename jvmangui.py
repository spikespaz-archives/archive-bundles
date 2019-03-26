import sys

from jvman.gui import AppMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("fusion")
    window = QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
