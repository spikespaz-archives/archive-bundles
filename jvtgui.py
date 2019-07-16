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
        # https://gist.github.com/lschmierer/443b8e21ad93e2a2d7eb

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
        PALETTE.setColor(QPalette.HighlightedText, Qt.black)

        if "accent-orange" in sys.argv:
            PALETTE.setColor(QPalette.Link, QColor(240, 83, 0))
            PALETTE.setColor(QPalette.Highlight, QColor(240, 83, 0))

            APP.setStyleSheet(
                """
                QToolTip {
                    color: #ffffff;
                    background-color: #F05300; #2a82da
                    border: 1px solid white;
                }
                """
            )
        else:
            PALETTE.setColor(QPalette.Link, QColor(42, 130, 218))
            PALETTE.setColor(QPalette.Highlight, QColor(42, 130, 218))

            APP.setStyleSheet(
                """
                QToolTip {
                    color: #ffffff;
                    background-color: #da732a;
                    border: 1px solid white;
                }
                """
            )
       
        APP.setPalette(PALETTE)

     

    if "accent-orange" in sys.argv:
        PALETTE = QPalette()

        # Color palette and stylesheet adapted from the gist below.
        # https://gist.github.com/lschmierer/443b8e21ad93e2a2d7eb

        

        APP.setPalette(PALETTE)

        APP.setStyleSheet(
            """
            QToolTip {
                color: #ffffff;
                background-color: #da732a;
                border: 1px solid white;
            }
            """
        )

    WINDOW.show()
    sys.exit(APP.exec_())
