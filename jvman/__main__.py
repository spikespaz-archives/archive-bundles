import sys


if __name__ == "__main__":
    if "gui" in sys.argv:
        from gui import AppMainWindow
        from PyQt5.QtWidgets import QApplication, QMainWindow

        app = QApplication([])
        window = QMainWindow()
        ui = AppMainWindow()
        ui.setupUi(window)
        window.show()
        sys.exit(app.exec_())
