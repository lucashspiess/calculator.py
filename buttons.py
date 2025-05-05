from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
import utils
import locale
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import Display
    from info import Info

class Button(QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px')
        self.setMinimumSize(55, 55)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info',  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]
        self.info = info
        self.display = display
        self._equation = ''
        self._left = None
        self._right = None
        self._op = None
        self._opSelected = False
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqTriggered.connect(self._eq)
        self.display.deleteTriggered.connect(self.display.backspace)
        self.display.inputTriggered.connect(self._insertTextToDisplay)
        self.display.operatorTriggered.connect(self._operatorClicked)

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not utils.isNumOrDot(buttonText) and not utils.isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertTextToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button: Button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button: Button):
        text = button.text()
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
        
        if text in '^+-*/':
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._operatorClicked, button.text())
                )
            
        if text == '=':
            self._connectButtonClicked(button, self._eq)

        if text == '⌫':
            self._connectButtonClicked(button, self.display.backspace)
        

    def _makeSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _insertTextToDisplay(self, text):
        if text not in '^/*-+=':
            if self._left is not None and self._right is not None:
                self._clear()
            if self._opSelected:
                self.display.clear()
                self._opSelected = False
            newDisplayValue = self.display.text() + text
            if not utils.isValidNumber(newDisplayValue):
                return
            self.display.insert(text)
            self.display.setFocus()

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = ''
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _operatorClicked(self, text):
        self._right = None
        displayText = self.display.text()
        buttonText = text

        if not utils.isValidNumber(displayText) and self._left is None:
            return
        
        if self._left is None:
            self._left = float(displayText)
            if self._left.is_integer():
                self._left = int(self._left)
        
        self._opSelected = True
        self._op = buttonText
        self.equation = f'{self._left} {self._op}'
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not utils.isValidNumber(displayText):
            return
        
        if self._right is None:
            self._right = float(displayText)
            if self._right.is_integer():
                self._right = int(self._right)

        self.equation = f'{self._left} {self._op} {self._right}'
        try:
            if '^' in self.equation and self._left is not None:
                result = math.pow(self._left, self._right)
            else:    
                result = eval(self.equation)
            result = float(result)
            if result.is_integer():
                result = int(result)
            self.display.setText(str(result))
            self._opSelected = True
        except ZeroDivisionError:
            self.display.setText('Não é possível dividir por 0')
        except OverflowError:
            self.display.setText('Número muito grande')
        self.info.setText(self.equation + ' =')
        self._left = result
        self.display.setFocus()
            