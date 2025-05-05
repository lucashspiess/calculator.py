from PySide6.QtWidgets import QApplication, QLabel, QLineEdit
from PySide6.QtGui import QIcon
from main_window import MainWindow
from variables import WINDOW_ICON_PATH
from display import Display
from info import Info
from styles import setupTheme
from buttons import Button, ButtonsGrid
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme(app)

    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info('')
    window.addWidgetToVLayout(info)

    display = Display()
    window.addWidgetToVLayout(display)

    buttonsGrid = ButtonsGrid(display, info)
    window.v_layout.addLayout(buttonsGrid)

    window.adjustFixedSize()

    window.show()
    app.exec()