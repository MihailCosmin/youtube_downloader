from json import load

from PySide6 import QtWidgets
from PySide6 import QtCore

from utils.common import clean_path


class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.setMinimumWidth(0)
        self.setMaximumWidth(0)

        self.settings_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.settings_layout)

        self.line1 = LineWidget()
        self.line2 = LineWidget()
        self.line3 = LineWidget()
        self.line4 = LineWidget()
        self.line5 = LineWidget()

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
        self.settings_layout1.setSpacing(20)

        self.appearance_label = QtWidgets.QLabel("Appearance")
        self.settings_widget1_1 = QtWidgets.QWidget()
        self.settings_layout1_1 = QtWidgets.QGridLayout(self.settings_widget1_1)
        self.download_label = QtWidgets.QLabel("Download")
        self.settings_widget1_2 = QtWidgets.QWidget()
        self.settings_layout1_2 = QtWidgets.QGridLayout(self.settings_widget1_2)
        self.ydl_options_basic = QtWidgets.QLabel("yt-dlp settings (Basic)")
        self.settings_widget1_3 = QtWidgets.QWidget()
        self.settings_widget1_3.setObjectName("settings_widget1_3")

        self.settings_layout1_3 = QtWidgets.QGridLayout(self.settings_widget1_3)

        self.settings_layout1.addWidget(self.settings_widget1_1)
        self.settings_layout1.addWidget(self.settings_widget1_2)

        self.settings_layout1_1.addWidget(self.appearance_label, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.line1, 1, 0, 1, 10)

        self.settings_layout1_2.addWidget(self.download_label, 0, 0, 1, 10, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.line2, 1, 0, 1, 20)

        self.settings_layout1_3.addWidget(self.ydl_options_basic, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_3.addWidget(self.line3, 1, 0, 1, 10)

        self.theme_label = QtWidgets.QLabel("Theme")
        self.theme_label.setObjectName(u"theme_label")
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.setObjectName(u"theme_combo")

        self.theme_combo.addItem("Dark")
        self.theme_combo.addItem("Light")
        self.theme_combo.setCurrentText(self.parent.config['theme'][0])

        self.settings_layout1_1.addWidget(self.theme_label, 2, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.theme_combo, 2, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.theme_combo.currentTextChanged.connect(
            lambda: self._change_setting(
                "change_theme",
                "theme",
                self.theme_combo.currentText()
            )
        )

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
        self.accent_combo.setCurrentText(self.parent.config["accent"][0])

        self.settings_layout1_1.addWidget(self.accent_label, 3, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_1.addWidget(self.accent_combo, 3, 1, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.accent_combo.currentTextChanged.connect(
            lambda: self._change_setting(
                "change_accent",
                "accent",
                self.accent_combo.currentText()
            )
        )

        self.download_location_label = QtWidgets.QLabel("Download Location")
        self.download_location_label.setObjectName(u"download_location_label")
        self.download_location = QtWidgets.QLineEdit()
        self.download_location.setObjectName(u"download_location")

        self.download_location.setMinimumWidth(self.settings_widget1_2.width() * 0.55)
        self.download_location.setMaximumWidth(self.settings_widget1_2.width() * 0.8)
        self.download_location.setReadOnly(True)

        self.download_location_button = QtWidgets.QPushButton(" . . . ")
        self.download_location_button.setObjectName(u"download_location_button")

        self.download_location_button.clicked.connect(self._set_download_location)

        self.settings_layout1_2.addWidget(self.download_location_label, 2, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.download_location, 2, 2, 1, 6, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout1_2.addWidget(self.download_location_button, 2, 8, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.settings_widget1_3.setMaximumWidth(self.parent.right_width * 0.39)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.settings_widget1_3)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.scroll_area.setMaximumWidth(self.parent.right_width * 0.333)
        self.scroll_area.setMinimumWidth(self.parent.right_width * 0.39)

        self.scroll_area.setMinimumHeight(self.parent.height * 0.9)
        self.scroll_area.setMaximumHeight(self.parent.height * 0.9)

        self.settings_layout1.addWidget(self.scroll_area)

        with open("src/ytb/yt-dlp_options.json", "r", encoding="utf-8") as _:
            options = load(_)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setMinimumWidth(self.settings_widget1_3.width() * 0.55)
        self.search_bar.setPlaceholderText("Filter settings...")

        self.search_bar.textChanged.connect(lambda: self._filter_settings(self.settings_layout1_3, self.ydl_options_basic, self.search_bar))
        self.settings_layout1_3.addWidget(self.search_bar, 0, 2, 1, 8, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        for index, (key, value) in enumerate(sorted(options.items(), key=lambda x: x[0])):
            if value["bae"] == "basic" and value["bae"] != "False":  # basic options
                self._create_setting(key, value, index, self.settings_widget1_3, self.settings_layout1_3)

        self.settings_layout1_3.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def _settings_widget2(self):
        self.youtube_dl_label1 = QtWidgets.QLabel("yt-dlp Options (Advanced)")
        self.settings_widget2_1 = QtWidgets.QWidget()
        self.settings_widget2_1.setObjectName("settings_widget2_1")

        self.settings_widget2_1.setMaximumWidth(self.parent.right_width * 0.39)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.settings_widget2_1)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.scroll_area.setMaximumWidth(self.parent.right_width * 0.333)
        self.scroll_area.setMinimumWidth(self.parent.right_width * 0.39)

        self.scroll_area.setMinimumHeight(self.parent.height * 0.9)
        self.scroll_area.setMaximumHeight(self.parent.height * 0.9)

        self.settings_layout2_1 = QtWidgets.QGridLayout(self.settings_widget2_1)
        self.settings_layout2.addWidget(self.scroll_area)

        self.settings_layout2_1.addWidget(self.youtube_dl_label1, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout2_1.addWidget(self.line4, 1, 0, 1, 10)

        with open("src/ytb/yt-dlp_options.json", "r", encoding="utf-8") as _:
            options = load(_)

        self.search_bar2 = QtWidgets.QLineEdit()
        self.search_bar2.setMinimumWidth(self.settings_widget2_1.width() * 0.55)
        self.search_bar2.setPlaceholderText("Filter settings...")

        self.search_bar2.textChanged.connect(lambda: self._filter_settings(self.settings_layout2_1, self.youtube_dl_label1, self.search_bar2))
        self.settings_layout2_1.addWidget(self.search_bar2, 0, 2, 1, 8, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        for index, (key, value) in enumerate(sorted(options.items(), key=lambda x: x[0])):
            if value["bae"] == "advanced" and value["add"] != "False":  # advanced options
                self._create_setting(key, value, index, self.settings_widget2_1, self.settings_layout2_1)

        self.settings_layout2_1.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def _settings_widget3(self):
        self.youtube_dl_label = QtWidgets.QLabel("yt-dlp Options (Expert)")
        self.settings_widget3_1 = QtWidgets.QWidget()
        self.settings_widget3_1.setObjectName("settings_widget3_1")

        self.settings_widget3_1.setMaximumWidth(self.parent.right_width * 0.39)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.settings_widget3_1)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.scroll_area.setMaximumWidth(self.parent.right_width * 0.333)
        self.scroll_area.setMinimumWidth(self.parent.right_width * 0.39)

        self.scroll_area.setMinimumHeight(self.parent.height * 0.9)
        self.scroll_area.setMaximumHeight(self.parent.height * 0.9)

        self.settings_layout3_1 = QtWidgets.QGridLayout(self.settings_widget3_1)
        self.settings_layout3.addWidget(self.scroll_area)
        self.settings_layout3_1.addWidget(self.youtube_dl_label, 0, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.settings_layout3_1.addWidget(self.line5, 1, 0, 1, 10)

        with open("src/ytb/yt-dlp_options.json", "r", encoding="utf-8") as _:
            options = load(_)

        self.search_bar3 = QtWidgets.QLineEdit()
        self.search_bar3.setMinimumWidth(self.settings_widget3_1.width() * 0.55)
        self.search_bar3.setPlaceholderText("Filter settings...")

        self.search_bar3.textChanged.connect(lambda: self._filter_settings(self.settings_layout3_1, self.youtube_dl_label, self.search_bar3))
        self.settings_layout3_1.addWidget(self.search_bar3, 0, 2, 1, 8, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        for index, (key, value) in enumerate(sorted(options.items(), key=lambda x: x[0])):
            if value["bae"] == "expert" and value["add"] != "False":  # expert options
                self._create_setting(key, value, index, self.settings_widget3_1, self.settings_layout3_1)

        self.settings_layout3_1.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def _set_download_location(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.download_location.setText(location)
        location = clean_path(location)
        self._change_setting(
            "change_download_location",
            "download_location",
            location,
            True
        )

    def _change_setting(self, func: str, key: str, value: str, youtube: bool = False):
        getattr(self.parent, func)(value)
        self.parent.update_config(key, value, youtube)

    @staticmethod
    def _filter_settings(layout: any, youtube_label: any, search_bar: any):
        for i in range(layout.count()):
            if layout.itemAt(i).widget() != youtube_label:
                if isinstance(layout.itemAt(i).widget(), QtWidgets.QLineEdit):
                    if search_bar.text().lower() in layout.itemAt(i).widget().objectName().lower():
                        layout.itemAt(i).widget().show()
                    elif layout.itemAt(i).widget() != search_bar:
                        layout.itemAt(i).widget().hide()
                if isinstance(layout.itemAt(i).widget(), QtWidgets.QComboBox):
                    if search_bar.text().lower() in layout.itemAt(i).widget().objectName().lower():
                        layout.itemAt(i).widget().show()
                    elif layout.itemAt(i).widget() != search_bar:
                        layout.itemAt(i).widget().hide()
                if isinstance(layout.itemAt(i).widget(), QtWidgets.QLabel):
                    if search_bar.text().lower() in layout.itemAt(i).widget().objectName().lower():
                        layout.itemAt(i).widget().show()
                    elif layout.itemAt(i).widget() != search_bar:
                        layout.itemAt(i).widget().hide()
                if isinstance(layout.itemAt(i).widget(), QtWidgets.QPushButton):
                    if search_bar.text().lower() in layout.itemAt(i).widget().objectName().lower():
                        layout.itemAt(i).widget().show()
                    elif layout.itemAt(i).widget() != search_bar:
                        layout.itemAt(i).widget().hide()

    def _create_setting(self, key: str, value: dict, index: int, widget: any, layout: any):
        browse_button = None
        label = QtWidgets.QLabel(key)
        label.setObjectName(f"{key}_label")
        label.setToolTip(value["description"])
        label.setWordWrap(True)
        label.setMinimumWidth(widget.width() * 0.3)

        label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        layout.addWidget(label, index + 2, 0, 1, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        if value["type"] == "bool" or value["type"] == "dropdown":
            line_edit = QtWidgets.QComboBox()
            line_edit.setObjectName(f"{key}_line_edit")

            line_edit.setMinimumWidth(widget.width() * 0.55)
            if value["type"] == "dropdown":
                for option in value["values"]:
                    line_edit.addItem(option)
            else:
                line_edit.addItem("True")
                line_edit.addItem("False")
            if key in self.parent.config:
                line_edit.setCurrentText(str(self.parent.config[key][0]))
            else:
                line_edit.setCurrentText(value["default"])
        elif value["type"] in ("filepath", "dirpath"):
            line_edit = QtWidgets.QPushButton("")
            line_edit.setObjectName(f"{key}_line_edit")
            line_edit.setMinimumWidth(widget.width() * 0.55)
            line_edit.setMaximumWidth(widget.width() * 0.8)
            if key in self.parent.config:
                line_edit.setText(self.parent.config[key][0])
                line_edit.setToolTip(self.parent.config[key][0])
            else:
                line_edit.setText(value["default"] if value["default"] not in ("None", "{}", "[]", None, "''") else "Click to set location")
                line_edit.setToolTip(value["default"] if value["default"] not in ("None", "{}", "[]", None, "''") else "Click to set location")
            line_edit.setFixedHeight(20)
            line_edit.clicked.connect(lambda: self._browse_file(line_edit, key))
        else:
            line_edit = QtWidgets.QLineEdit()
            line_edit.setObjectName(f"{key}_line_edit")
            line_edit.setMinimumWidth(widget.width() * 0.55)
            line_edit.setMaximumWidth(widget.width() * 0.8)
            if key in self.parent.config:
                line_edit.setText(str(self.parent.config[key][0]))
            else:
                line_edit.setText(value["default"] if value["default"] not in ("None", "{}", "[]", None, "''") else "")
        layout.addWidget(line_edit, index + 2, 2, 1, 6, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        if browse_button:
            layout.addWidget(browse_button, index + 2, 8, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

    def _browse_file(self, line_edit: any, key: str):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", line_edit.text(), "All Files (*)")
        if file[0]:
            line_edit.setText(file[0])
            line_edit.setToolTip(file[0])
            self._change_setting(
                "change_setting",
                key,
                file[0]
            )

class LineWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
