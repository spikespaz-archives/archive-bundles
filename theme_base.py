#! /usr/bin/env python3

from PyQt5.QtGui import QPalette, QColor


class QThemePalette(QPalette):
    def __init__(self):
        super().__init__()

        self.setColor(QPalette.Window,          QColor(*self.c_window))
        self.setColor(QPalette.WindowText,      QColor(*self.c_window_text))
        self.setColor(QPalette.Base,            QColor(*self.c_base))
        self.setColor(QPalette.AlternateBase,   QColor(*self.c_base_alternate))
        self.setColor(QPalette.ToolTipBase,     QColor(*self.c_tool_tip_base))
        self.setColor(QPalette.ToolTipText,     QColor(*self.c_tool_tip_text))
        self.setColor(QPalette.Text,            QColor(*self.c_text))
        self.setColor(QPalette.Button,          QColor(*self.c_button))
        self.setColor(QPalette.ButtonText,      QColor(*self.c_button_text))
        self.setColor(QPalette.BrightText,      QColor(*self.c_bright_text))
        self.setColor(QPalette.Link,            QColor(*self.c_link_text))
        self.setColor(QPalette.Highlight,       QColor(*self.c_highlight))
        self.setColor(QPalette.HighlightedText, QColor(*self.c_highlight_text))

    def set_stylesheet(self, app):
        """Set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet("QToolTip {{" +
                          "color:            rgb({}, {}, {});".format(*self.c_tooltip_text) +
                          "background-color: rgb({}, {}, {});".format(*self.c_tooltip) +
                          "border: 1px solid rgb({}, {}, {});".format(*self.c_tooltip_border) +
                          "}}")

    def set_app(self, app):
        """Set the theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle("Fusion")
        app.setPalette(self)
        self.set_stylesheet(app)
