from PyQt5.QtWidgets import QButtonGroup


class CheckBoxButtonGroup(QButtonGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setExclusive(False)
        self.buttonToggled.connect(self.reset)

    def addButton(self, button, *args, **kwargs):
        super().addButton(button, *args, **kwargs)

        self.reset()

    def checked_buttons(self):
        return [button for button in self.buttons() if button.isChecked()]

    def reset(self, *args, **kwargs):
        checked = self.checked_buttons()

        if len(checked) == 1:
            checked[0].setEnabled(False)
        else:
            for button in checked:
                button.setEnabled(True)
