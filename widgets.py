from PyQt5.QtWidgets import QButtonGroup


class CheckBoxButtonGroup(QButtonGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setExclusive(False)
        self.buttonToggled.connect(self.__protect_remaining)

    def addButton(self, button, *args, **kwargs):
        super().addButton(button, *args, **kwargs)

        self.__protect_remaining(button, button.isChecked())

    def __protect_remaining(self, button, checked):
        checked_buttons = self.checked_buttons()

        if checked:
            for button in checked_buttons:
                button.setEnabled(True)
        elif len(checked_buttons) == 1:
            checked_buttons[0].setEnabled(False)

    def checked_buttons(self):
        return [button for button in self.buttons() if button.isChecked()]

    def reset(self):
        checked = self.checked_buttons()

        if len(checked) == 1:
            checked[0].setEnabled(False)
        else:
            for button in checked:
                button.setEnabled(True)
