from PySide6 import QtWidgets
from PySide6 import QtCore

def format_button(button, width: int = 80, height: int = 30):
    button.setFixedHeight(height)
    button.setFixedWidth(width)
    button.move(0, 0)
    button.raise_()
    button.setFlat(True)
    button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2))
    button.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    button.setWindowOpacity(0.5)
    button.setMouseTracking(True)

    # on hover 
    button.enterEvent = lambda event: button.setWindowOpacity(1)
    button.leaveEvent = lambda event: button.setWindowOpacity(0.5)

    return button

def format_button_transparent(button):
    button.setWindowOpacity(0.0)
    button.setStyleSheet("QPushButton {border: 0px solid #ffffff;}")
    return button

def format_loading_bar(bar, height: int = 26, width: int = 52):
    bar.setMinimum(0)
    bar.setMaximum(100)
    bar.setValue(0)
    bar.setTextVisible(False)
    bar.setMinimumHeight(height)
    bar.setFixedWidth(width)
    #bar.setStyleSheet("QProgressBar {border: 1px solid #ffffff; border-radius: 5px; text-align: right;}")
    #bar.setStyleSheet("QProgressBar::chunk {background-color: #000000; width: 10px;}")
    bar.setAlignment(QtCore.Qt.AlignCenter)

    return bar