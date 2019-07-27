import sys

from jvtgui.gui import AppMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


if __name__ == "__main__":
    APP = QApplication([])
    WINDOW = AppMainWindow()

    print(sys.argv)

    if "fusion" in sys.argv:
        APP.setStyle("fusion")

    if "fusion-dark" in sys.argv:
        PALETTE = QPalette()

        # Color palette and stylesheet adapted from the gist below.
        # https://gist.github.com/QuantumCD/6245215

        if "accent-orange" in sys.argv:
            ACCENT_COLOR = (240, 83, 0)
        else:
            ACCENT_COLOR = (42, 130, 218)

        PALETTE.setColor(QPalette.Window, QColor(53, 53, 53))
        PALETTE.setColor(QPalette.WindowText, Qt.white)
        PALETTE.setColor(QPalette.Base, QColor(45, 45, 45))
        PALETTE.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        PALETTE.setColor(QPalette.ToolTipBase, Qt.white)
        PALETTE.setColor(QPalette.ToolTipText, Qt.white)
        PALETTE.setColor(QPalette.Text, Qt.white)
        PALETTE.setColor(QPalette.Button, QColor(53, 53, 53))
        PALETTE.setColor(QPalette.ButtonText, Qt.white)
        PALETTE.setColor(QPalette.BrightText, Qt.red)
        PALETTE.setColor(QPalette.Link, QColor(*ACCENT_COLOR))

        PALETTE.setColor(QPalette.Highlight, QColor(*ACCENT_COLOR))
        PALETTE.setColor(QPalette.HighlightedText, Qt.black)

        APP.setStyleSheet(
            """
            QToolTip {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #{accent_color[0]:02x}{accent_color[1]:02x}{accent_color[2]:02x};
            }
            /* QFrame::HLine, QFrame::VLine */
            QFrame[frameShape="4"][frameShadow="48"],
            QFrame[frameShape="5"][frameShadow="48"] {
                background-color: #2d2d2d;
            }
            """
        )

        APP.setPalette(PALETTE)

    WINDOW.show()
    sys.exit(APP.exec_())
