import sys

from jvman.gui import AppMainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("fusion")
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())
