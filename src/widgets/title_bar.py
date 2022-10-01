from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QFrame

from PySide6.QtCore import Qt
from PySide6.QtCore import QEvent

from PySide6.QtGui import QMouseEvent

class TitleBar(QWidget):
    """TitleBar

    Args:
        QWidget (_type_): QWidget
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar = QFrame()
        self.title_bar.setLayout(self.title_bar_layout)
        self.title_bar.setObjectName(u"title_bar")

        self.title_handle_bar = HandleBar(parent=self.parent)


        self.minimize_button = QPushButton()
        self.maximize_button = QPushButton()
        self.exit_button = QPushButton()

        self.minimize_button.setObjectName(u"minimize_button")
        self.maximize_button.setObjectName(u"maximize_button")
        self.exit_button.setObjectName(u"exit_button")

        self.minimize_button.setMaximumWidth(20)
        self.maximize_button.setMaximumWidth(20)
        self.exit_button.setMaximumWidth(20)

        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.maximize_button.clicked.connect(self.parent.toggleMaximizeRestore)
        self.exit_button.clicked.connect(self.parent.close)

        self.title_bar_layout.addWidget(self.title_handle_bar)
        self.title_bar_layout.addWidget(self.minimize_button)
        self.title_bar_layout.addWidget(self.maximize_button)
        self.title_bar_layout.addWidget(self.exit_button)

        self.layout.addWidget(self.title_bar)

class HandleBar(QWidget):
    """HandleBar

    Args:
        QWidget (QWidget): QWidget
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.setObjectName(u"title_handle_bar")

    def mouseDoubleClickEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.parent.toggleMaximizeRestore()
                event.accept()

    def mousePressEvent(self, event):
        if not self.parent.isMaximized():
            self.parent.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.parent.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.parent.move(self.parent.pos() + event.globalPosition().toPoint() - self.parent.dragPos)
                self.parent.dragPos = event.globalPosition().toPoint()
                event.accept()
