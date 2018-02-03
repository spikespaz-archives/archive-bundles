from PyQt5 import QtWidgets
from interface import Ui_batch_media_converter
import sys


class Interface(Ui_batch_media_converter):
    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.exit_button.clicked.connect(exit)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    interface = Interface()
    interface.setupUi(main_window)
    main_window.show()

    sys.exit(app.exec_())

