from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variables import BIG_FONT_SIZE, MARGINS, MINIMUN_WIDTH
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLineEdit
from utils import isNumOrDot

class Display(QLineEdit):
    eqTriggered = Signal()
    deleteTriggered = Signal()
    inputTriggered = Signal(str)
    operatorTriggered = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUN_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[MARGINS for _ in range(4)])
        self.focusWidget()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        text = event.text()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Delete, KEYS.Key_Backspace] 

        if isEnter or text == '=':
            self.eqTriggered.emit()
            return event.ignore()
        
        if isDelete:
            self.deleteTriggered.emit()
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputTriggered.emit(text)
            return event.ignore()
        
        if text in '/*-+^':
            self.operatorTriggered.emit(text)
            return event.ignore()