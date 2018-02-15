#! /usr/bin/env python3

from PyQt5.QtGui import QPalette, QColor
from os import path
from json import load

THEME_PATH = path.abspath("themes/")


def _css_rgb(color, a=False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""
    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())


class QThemePalette(QPalette):
    """Load a theme from `./themes/` based on name provided."""
    def __init__(self, theme_name="fusiondark"):
        super().__init__()

        self.theme = path.join(THEME_PATH, theme_name)

        theme_dict = load(THEME_PATH)

        self.basetheme = theme_dict["basetheme"]
        self.foreground = QColor(*theme_dict["foreground"])
        self.foreground2 = QColor(*theme_dict["foreground2"])
        self.background = QColor(*theme_dict["background"])
        self.background2 = QColor(*theme_dict["background2"])
        self.accent = QColor(*theme_dict["accent"])
        self.accent2 = QColor(*theme_dict["accent2"])
        self.tooltip = theme_dict["tooltip"]

        self.setColor(QPalette.Window,          self.background)
        self.setColor(QPalette.WindowText,      self.foreground)
        self.setColor(QPalette.Base,            self.background2)
        self.setColor(QPalette.AlternateBase,   self.background)
        self.setColor(QPalette.ToolTipBase,     self.foreground)
        self.setColor(QPalette.ToolTipText,     self.foreground)
        self.setColor(QPalette.Text,            self.foreground)
        self.setColor(QPalette.Button,          self.background)
        self.setColor(QPalette.ButtonText,      self.foreground)
        self.setColor(QPalette.BrightText,      self.accent2)
        self.setColor(QPalette.Link,            self.accent)
        self.setColor(QPalette.Highlight,       self.accent)
        self.setColor(QPalette.HighlightedText, self.background2)

    def set_stylesheet(self, app):
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet(self.tooltip.format(
            foreground=_css_rgb(self.foreground),
            foreground2=_css_rgb(self.foreground2),
            background=_css_rgb(self.background),
            background2=_css_rgb(self.background2),
            accent=_css_rgb(self.accent),
            accent2=_css_rgb(self.accent2)))

    def set_app(self, app):
        """Set the theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle(self.basetheme)
        app.setPalette(self)
        self.set_stylesheet(app)

