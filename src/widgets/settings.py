from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from utils.format import format_button

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.settings_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.settings_layout)
        self.settings_top_widget = QtWidgets.QWidget()
        self.settings_top_layout = QtWidgets.QHBoxLayout(self.settings_top_widget)
        self.settings_layout.addWidget(self.settings_top_widget)
        # self.settings_top_widget.setStyleSheet("QWidget {border: 1px solid #ffffff; border-radius: 5px;}")
        self.settings_top_widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2))

        self.settings_layout.setStretch(0, 9)

        self.setMinimumWidth(self.parent._right_width)
        self.setMaximumWidth(self.parent._right_width)

        self.settings_bottom_widget = QtWidgets.QWidget()
        self.settings_bottom_layout = QtWidgets.QHBoxLayout(self.settings_bottom_widget)
        self.settings_layout.addWidget(self.settings_bottom_widget)
        self.settings_bottom_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.apply_button = QtWidgets.QPushButton("Apply")
        self.apply_button = format_button(self.apply_button)
        self.settings_bottom_layout.addWidget(self.apply_button)
        self.apply_button.clicked.connect(self._show_browser)

        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button = format_button(self.close_button)
        self.settings_bottom_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self._show_browser)

        self.apply_button.move(self.parent._right_width - self.apply_button.width() - 10, 0)
        self.close_button.move(self.parent._right_width - self.close_button.width() - 10, 30)

    def _show_browser(self):
        self.parent.settings_widget.hide()
        self.parent.webview.show()

    def _show_settings(self):
        self.parent.webview.hide()
        self.parent.right_widget.right_layout.addWidget(self.parent.settings_widget)
        self.parent.settings_widget.show()
