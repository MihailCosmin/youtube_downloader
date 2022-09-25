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

        # self.settings_widget1 = QtWidgets.QWidget()
        # self.settings_widget1.setObjectName(u"settings_widget1")

        # self.settings_widget2 = QtWidgets.QWidget()
        # self.settings_widget2.setObjectName(u"settings_widget2")

        # self.settings_widget3 = QtWidgets.QWidget()
        # self.settings_widget3.setObjectName(u"settings_widget3")

        # add three vertical layouts inside the horizontal layout
        # self.settings_layout1 = QtWidgets.QVBoxLayout(self.settings_widget1)
        # self.settings_layout2 = QtWidgets.QGridLayout(self.settings_widget2)
        # self.settings_layout3 = QtWidgets.QGridLayout(self.settings_widget3)
        self.settings_layout1 = QtWidgets.QVBoxLayout()
        self.settings_layout2 = QtWidgets.QGridLayout()
        self.settings_layout3 = QtWidgets.QGridLayout()

        # self.settings_layout.addWidget(self.settings_widget1)
        # self.settings_layout.addWidget(self.settings_widget2)
        # self.settings_layout.addWidget(self.settings_widget3)

        self.settings_layout.addLayout(self.settings_layout1)
        self.settings_layout.addLayout(self.settings_layout2)
        self.settings_layout.addLayout(self.settings_layout3)

        self._settings_widget3()

    def _settings_widget3(self):
        self.appearance_label = QtWidgets.QLabel("Appearance")
        self.settings_layout1_1 = QtWidgets.QGridLayout()
        self.download_label = QtWidgets.QLabel("Download")
        self.settings_layout1_2 = QtWidgets.QGridLayout()
        self.settings_layout1.addLayout(self.settings_layout1_1)
        self.settings_layout1.addLayout(self.settings_layout1_2)
        self.settings_layout1_1.addWidget(self.appearance_label, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        # set space between the layouts
        self.settings_layout1.setSpacing(20)
        self.settings_layout1_2.addWidget(self.download_label, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.theme_label = QtWidgets.QLabel("Theme")
        self.theme_label.setObjectName(u"theme_label")
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.setObjectName(u"theme_combo")

        self.theme_combo.addItem("Dark")
        self.theme_combo.addItem("Light")

        self.settings_layout1_1.addWidget(self.theme_label, 1, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.theme_combo, 1, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.theme_combo.currentTextChanged.connect(lambda: self.parent.change_theme(self.theme_combo.currentText()))
        
        # add a label and a drop down for accent color
        self.accent_label = QtWidgets.QLabel("Accent Color")
        self.accent_label.setObjectName(u"accent_label")
        self.accent_combo = QtWidgets.QComboBox()
        self.accent_combo.setObjectName(u"accent_combo")
        self.accent_combo.addItem("Blue")
        self.accent_combo.addItem("Red")
        self.accent_combo.addItem("Green")
        self.accent_combo.addItem("Yellow")
        self.accent_combo.addItem("Orange")
        self.accent_combo.addItem("Purple")
        self.accent_combo.addItem("Pink")
        
        self.settings_layout1_1.addWidget(self.accent_label, 2, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.accent_combo, 2, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        
        self.theme_combo.currentTextChanged.connect(lambda: self.parent.change_accent(self.accent_combo.currentText()))
