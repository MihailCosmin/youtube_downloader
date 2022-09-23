from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QFrame

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

        self.title_handle_bar = QFrame()
        self.title_handle_bar.setObjectName(u"title_handle_bar")

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
        self.title_handle_bar.mouseMoveEvent = self.parent.mouseMoveEvent
