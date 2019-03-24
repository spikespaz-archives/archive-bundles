from main import *


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    ui = AppMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
