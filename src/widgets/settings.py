from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from utils.format import format_button

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setMinimumWidth(0)
        self.setMaximumWidth(0)

        self.settings_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.settings_layout)

        self.settings_widget1 = QtWidgets.QWidget()
        self.settings_widget1.setObjectName(u"settings_widget1")

        self.settings_widget2 = QtWidgets.QWidget()
        self.settings_widget2.setObjectName(u"settings_widget2")

        self.settings_widget3 = QtWidgets.QWidget()
        self.settings_widget3.setObjectName(u"settings_widget3")

        # add three vertical layouts inside the horizontal layout
        self.settings_layout1 = QtWidgets.QGridLayout(self.settings_widget1)
        self.settings_layout2 = QtWidgets.QGridLayout(self.settings_widget2)
        self.settings_layout3 = QtWidgets.QGridLayout(self.settings_widget3)

        self.settings_layout.addWidget(self.settings_widget1)
        self.settings_layout.addWidget(self.settings_widget2)
        self.settings_layout.addWidget(self.settings_widget3)

    
    def _settings_widget3(self):
        # add 

