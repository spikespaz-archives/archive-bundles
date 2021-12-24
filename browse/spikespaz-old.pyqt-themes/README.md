# pyqt-themes
Small script that provides a structure for easily creating themes with PyQt5.

Use this with `git sobmodule add http://git.spikespaz.com/pyqt-themes themes` and import from the `themes` module.

Now you can use `<theme>.set_app(<application>)` where `<theme>` is an instance of `themes.QThemePalette` and `<application>` is an instance of `PyQt5.QtWidgets.QApplication`.

| Class Variable       | Qt Class                                                |
| -------------------- | ------------------------------------------------------- |
| `c_window`           | `PyQt5.QtGui.QPalette.Window`                           |
| `c_window_text`      | `PyQt5.QtGui.QPalette.WindowText`                       |
| `c_base`             | `PyQt5.QtGui.QPalette.Base`                             |
| `c_base_alternate`   | `PyQt5.QtGui.QPalette.AlternateBase`                    |
| `c_tool_tip_base`    | `PyQt5.QtGui.QPalette.ToolTipBase`                      |
| `c_tool_tip_text`    | `PyQt5.QtGui.QPalette.ToolTipText`                      |
| `c_text`             | `PyQt5.QtGui.QPalette.Text`                             |
| `c_button`           | `PyQt5.QtGui.QPalette.Button`                           |
| `c_button_text`      | `PyQt5.QtGui.QPalette.ButtonText`                       |
| `c_bright_text`      | `PyQt5.QtGui.QPalette.BrightText`                       |
| `c_link_text`        | `PyQt5.QtGui.QPalette.Link`                             |
| `c_highlight`        | `PyQt5.QtGui.QPalette.Highlight`                        |
| `c_highlight_text`   | `PyQt5.QtGui.QPalette.HighlightedText`                  |
| `c_tooltip_text`     | `QToolTip {color: rgb(<c_tool_tip_text>)`               |
| `c_tooltip`          | `QToolTip {background-color: rgb(<c_tool_tip>)`         |
| `c_tooltip_border`   | `QToolTip {border: 1px solid rgb(<c_tool_tip_border>)`  |
