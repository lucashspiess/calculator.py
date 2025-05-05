import qdarkstyle
from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)
 
qss = f"""
    QPushButton{{
        color: {PRIMARY_COLOR};
        background: #19232D;
        border: 1px solid {PRIMARY_COLOR};
    }}
    QPushButton:hover{{
        color: {PRIMARY_COLOR};
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
    QLineEdit:focus{{
        border: 1px solid {PRIMARY_COLOR};
    }}
    QLineEdit{{
        border: 1px solid {PRIMARY_COLOR};
    }}
"""
 
 
def setupTheme(app):
    # Aplicar o estilo escuro do qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    # Sobrepor com o QSS personalizado para estilização adicional
    app.setStyleSheet(app.styleSheet() + qss)