import sys

from jvman.gui import AppMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# https://gist.github.com/lschmierer/443b8e21ad93e2a2d7eb

if __name__ == "__main__":
    APP = QApplication([])
    WINDOW = AppMainWindow()
    PALETTE = QPalette()

    PALETTE.setColor(QPalette.Window, QColor(53, 53, 53))
    PALETTE.setColor(QPalette.WindowText, Qt.white)
    PALETTE.setColor(QPalette.Base, QColor(25, 25, 25))
    PALETTE.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    PALETTE.setColor(QPalette.ToolTipBase, Qt.white)
    PALETTE.setColor(QPalette.ToolTipText, Qt.white)
    PALETTE.setColor(QPalette.Text, Qt.white)
    PALETTE.setColor(QPalette.Button, QColor(53, 53, 53))
    PALETTE.setColor(QPalette.ButtonText, Qt.white)
    PALETTE.setColor(QPalette.BrightText, Qt.red)
    PALETTE.setColor(QPalette.Link, QColor(42, 130, 218))
    PALETTE.setColor(QPalette.Highlight, QColor(42, 130, 218))
    PALETTE.setColor(QPalette.HighlightedText, Qt.black)

    APP.setStyle("fusion")
    APP.setPalette(PALETTE)

    APP.setStyleSheet(
        """
        QToolTip {
            color: #ffffff;
            background-color: #2a82da;
            border: 1px solid white;
        }
        """
    )

    WINDOW.show()
    sys.exit(APP.exec_())
