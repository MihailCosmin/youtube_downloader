from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setMinimumWidth(0)
        self.setMaximumWidth(0)

        self.settings_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.settings_layout)

        self.settings_layout1 = QtWidgets.QVBoxLayout()
        self.settings_layout2 = QtWidgets.QGridLayout()
        self.settings_layout3 = QtWidgets.QGridLayout()

        self.settings_layout.addLayout(self.settings_layout1)
        self.settings_layout.addLayout(self.settings_layout2)
        self.settings_layout.addLayout(self.settings_layout3)

        self.settings_layout.setSpacing(20)

        self._settings_widget1()
        self._settings_widget2()
        self._settings_widget3()

    def _settings_widget1(self):
        self.appearance_label = QtWidgets.QLabel("Appearance")
        self.settings_widget1_1 = QtWidgets.QWidget()
        self.settings_layout1_1 = QtWidgets.QGridLayout(self.settings_widget1_1)
        self.download_label = QtWidgets.QLabel("Download")
        self.settings_widget1_2 = QtWidgets.QWidget()
        self.settings_layout1_2 = QtWidgets.QGridLayout(self.settings_widget1_2)

        self.settings_layout1.addWidget(self.settings_widget1_1)
        self.settings_layout1.addWidget(self.settings_widget1_2)
        self.settings_layout1_1.addWidget(self.appearance_label, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.line1 = LineWidget()
        self.line2 = LineWidget()
        self.settings_layout1_1.addWidget(self.line1, 1, 0, 1, 2)

        self.settings_layout1.setSpacing(20)
        self.settings_layout1_2.addWidget(self.download_label, 0, 0, 1, 10, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.line2, 1, 0, 1, 2)

        self.theme_label = QtWidgets.QLabel("Theme")
        self.theme_label.setObjectName(u"theme_label")
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.setObjectName(u"theme_combo")

        self.theme_combo.addItem("Dark")
        self.theme_combo.addItem("Light")

        self.settings_layout1_1.addWidget(self.theme_label, 2, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.theme_combo, 2, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.theme_combo.currentTextChanged.connect(lambda: self.parent.change_theme(self.theme_combo.currentText()))

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

        self.settings_layout1_1.addWidget(self.accent_label, 3, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.accent_combo, 3, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.theme_combo.currentTextChanged.connect(lambda: self.parent.change_accent(self.accent_combo.currentText()))

        self.download_location_label = QtWidgets.QLabel("Download Location")
        self.download_location_label.setObjectName(u"download_location_label")
        self.download_location = QtWidgets.QLineEdit()
        self.download_location.setObjectName(u"download_location")

        self.download_location.setMinimumWidth(self.settings_widget1_2.width() * 0.6)
        self.download_location.setMaximumWidth(self.settings_widget1_2.width() * 0.8)
        self.download_location.setReadOnly(True)

        self.download_location_button = QtWidgets.QPushButton(" . . . ")
        self.download_location_button.setObjectName(u"download_location_button")
        self.download_location_button.clicked.connect(self.set_download_location)

        self.settings_layout1_2.addWidget(self.download_location_label, 2, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.download_location, 2, 2, 1, 6, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.download_location_button, 2, 8, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.settings_layout1_2.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def _settings_widget2(self):
        self.settings_widget2_1 = QtWidgets.QWidget()
        self.settings_layout2_1 = QtWidgets.QGridLayout(self.settings_widget2_1)
        self.settings_layout2.addWidget(self.settings_widget2_1)

    def _settings_widget3(self):
        self.settings_widget3_1 = QtWidgets.QWidget()
        self.settings_layout3_1 = QtWidgets.QGridLayout(self.settings_widget3_1)
        self.settings_layout3.addWidget(self.settings_widget3_1)

    def set_download_location(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        print(f"location: {location}")
        self.download_location.setText(location)


class LineWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)