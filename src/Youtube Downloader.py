from os import mkdir
from os import listdir
from os.path import sep
from os.path import isdir
from os.path import isfile
from os.path import dirname
from os.path import splitext
from os.path import realpath
from os.path import basename
from os.path import expanduser

from re import findall
from re import sub

import sys
from sys import executable

from json import dump
from json import load

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMenu

from PySide6.QtWebEngineCore import QWebEnginePage

from PySide6.QtNetwork import QNetworkCookie

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QThreadPool
from PySide6.QtCore import QPoint
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt

from PySide6.QtGui import QIcon

exe = ''
if splitext(basename(__file__))[1] == '.pyw'\
        or splitext(basename(__file__))[1] == '.py':
    exe = dirname(realpath(__file__))
elif splitext(basename(__file__))[1] == '.exe':
    exe = dirname(executable)
sys.path.append(exe)

from ytb.youtube import YoutubeDLP

from utils.thread import Worker
from utils.format import format_loading_bar

from widgets.center import CenterWidget
from widgets.settings import SettingsWidget
from widgets.left import LeftWidget
from widgets.right import RightWidget
from widgets.title_bar import TitleBar
from widgets.left_menu import LeftMenu
from widgets.dialogs import BubbleLabel

from utils.common import clean_path

ACCENT = r'	color: [a-z]+;'
SVG_FILL = r' fill="[a-z]+" '

class YoutubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('src/images/icons/youtube_downloader_big.png'))

        self.config = {}
        self._init_config()

        self.height = QApplication.primaryScreen().size().height()
        self.left_bar_width = 50
        self.left_width = round(
            (QApplication.primaryScreen().size().width() - self.left_bar_width) * 0.17,
            0)
        self.right_width = round(
            (QApplication.primaryScreen().size().width() - self.left_bar_width) * 0.83,
            0)

        self.dragPos = QPoint()
        self.bubble = BubbleLabel()

        self.title_bar = TitleBar(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.queue = []
        self.worker = None
        self.threadpool = QThreadPool()
        self.progress_bar = None

        self.setObjectName(u"main_window")

        self.setWindowTitle("Youtube Downloader")
        self.setMaximumWidth(QApplication.primaryScreen().size().width())

        self.central_widget = CenterWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.app_layout = QHBoxLayout()
        self.app_layout.setContentsMargins(0, 10, 0, 10)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.app_layout)
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_widget = SettingsWidget(parent=self)
        self.settings_widget.setObjectName(u"settings_widget")

        self.left_widget = LeftWidget(parent=self)
        self.left_widget.setObjectName(u"left_widget")

        self.right_widget = RightWidget(parent=self)

        self.ydl = YoutubeDLP()

        self.left_menu_frame = LeftMenu(parent=self)
        self.app_layout.addWidget(self.left_menu_frame)
        self.app_layout.addWidget(self.left_widget)
        self.app_layout.addWidget(self.settings_widget)
        self.app_layout.addWidget(self.right_widget)

        self.app_layout.setAlignment(Qt.AlignLeft)

        with open(f"src/themes/{self.config['theme'][0]}.qss", "r", encoding="utf-8") as _:
            stylesheet = _.read()
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.showMaximized()

    def _init_config(self):
        if not isfile("src/config/config.json"):
            self.config = {
                "download_location": (clean_path(expanduser("~/Downloads")), True),
                "theme": ("Dark", False),
                "accent": ("Red", False),
                "ffmpeg_location": ("3rd/ffmpeg.exe", True),
            }
            if not isdir("src/config"):
                mkdir("src/config")
            with open("src/config/config.json", "w", encoding="utf-8") as _:
                dump(self.config, _, indent=4)
        else:
            with open("src/config/config.json", "r", encoding="utf-8") as _:
                self.config = load(_)

    def update_config(self, key: str, value, youtube: bool):
        self.config[key] = (value, youtube)
        if youtube:
            self.ydl.update_dl_ops(key, value)
        with open("src/config/config.json", "w", encoding="utf-8") as _:
            dump(self.config, _, indent=4)

    def toggleMaximizeRestore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def toggle_settings(self):
        if self.settings_widget.width() != 0:
            self.settings_widget.setMinimumWidth(0)
            self.settings_widget.setMaximumWidth(0)
            self.left_widget.setMaximumWidth(0)
            self.left_widget.setMinimumWidth(0)
            self.right_widget.setMaximumWidth(self.right_width + self.left_width)
            self.right_widget.setMinimumWidth(self.right_width + self.left_width)
            self.central_widget.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.central_widget.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.animation = QPropertyAnimation(self.webview, b"maximumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(0)
            self.animation.setEndValue(QApplication.primaryScreen().size().width())
            self.animation.setEasingCurve(QEasingCurve.BezierSpline)
            self.animation.start()
        else:
            self.webview.setMaximumWidth(0)
            self.webview.setMinimumWidth(0)
            self.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.left_widget.setMaximumWidth(0)
            self.left_widget.setMinimumWidth(0)
            self.right_widget.setMaximumWidth(0)
            self.right_widget.setMinimumWidth(0)
            self.animation = QPropertyAnimation(self.settings_widget, b"minimumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.right_width + self.left_width)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

        self.save_settings()

    def save_settings(self):
        """save_settings
        """
        with open("src/ytb/yt-dlp_options.json", "r", encoding="utf-8") as _:
            opt = load(_)
        for key, value in opt.items():
            try:
                if value["type"] in ("bool", "dropdown"):
                    if key not in self.config:
                        if str(self.findChild(QComboBox, f"{key}_line_edit").currentText()) != value["default"]:
                            self.update_config(key, self.findChild(QComboBox, f"{key}_line_edit").currentText(), True)
                    elif str(self.findChild(QComboBox, f"{key}_line_edit").currentText()) != self.config[key]:
                        self.update_config(key, self.findChild(QComboBox, f"{key}_line_edit").currentText(), True)
            except AttributeError:
                pass
            try:
                if value["type"] in ("filepath", "dirpath"):
                    if key not in self.config:
                        if self.findChild(QPushButton, f"{key}_line_edit").text() not in (value["default"], "", "Click to set location"):
                            self.update_config(key, self.findChild(QPushButton, f"{key}_line_edit").text(), True)
                    elif self.findChild(QPushButton, f"{key}_line_edit").text() != self.config[key]:
                        self.update_config(key, self.findChild(QPushButton, f"{key}_line_edit").text(), True)
                elif value["type"] not in ("bool", "dropdown"):
                    if key not in self.config:
                        if self.findChild(QLineEdit, f"{key}_line_edit").text() not in (value["default"], ""):
                            setting = int(self.findChild(QLineEdit, f"{key}_line_edit").text().strip()) if value["type"] == "int" else self.findChild(QLineEdit, f"{key}_line_edit").text().strip()
                            self.update_config(key, setting, True)
                    elif self.findChild(QLineEdit, f"{key}_line_edit").text() != self.config[key]:
                        self.update_config(key, self.findChild(QLineEdit, f"{key}_line_edit").text(), True)
            except AttributeError:
                pass

    def toggle_downloads(self):
        if self.left_widget.width() != 0:
            self.left_widget.setMinimumWidth(0)
            self.central_widget.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.central_widget.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.setMinimumWidth(QApplication.primaryScreen().size().width())

            self.animation = QPropertyAnimation(self.left_widget, b"maximumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(self.left_widget.width())
            self.animation.setEndValue(0)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

            self.animation.finished.connect(self._restore_youtube1)

        else:
            self.settings_widget.setMinimumWidth(0)
            self.settings_widget.setMaximumWidth(0)
            self.animation = QPropertyAnimation(self.left_widget, b"minimumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.left_width)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()
            self.animation.finished.connect(self._restore_youtube2)
        self.save_settings()

    def _restore_youtube1(self):
        self.right_widget.setMaximumWidth(self.right_width + self.left_width)
        self.right_widget.setMinimumWidth(self.right_width + self.left_width)

        self.webview.setMaximumWidth(self.right_width + self.left_width)
        self.webview.setMinimumWidth(self.right_width + self.left_width)

    def _restore_youtube2(self):
        self.webview.setMaximumWidth(self.right_width)
        self.webview.setMinimumWidth(self.right_width)

        self.right_widget.setMaximumWidth(self.right_width)
        self.right_widget.setMinimumWidth(self.right_width)

    def _download_queue(self, progress_bar=None):
        if self.progress_bar is not None:
            self.progress_bar.hide()
        if self.queue:
            self.progress_bar = progress_bar
            self.progress_bar.show()
            self.progress_bar.setTextVisible(True)
            self.progress_bar.setFormat("Download starting...")
            self.progress_bar.setValue(0)

            self.worker = Worker(
                self._download_single_queue,
                progress=True,
                console=False,
            )
            self.worker.signals.progress.connect(self._progress_bar_update)
            self.worker.signals.finished.connect(self._thread_complete)
            self.threadpool.start(self.worker)
        else:
            self.bubble.setText("Queue is empty")
            self.bubble.show()

    def _thread_complete(self):
        self.progress_bar.setValue(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Done")

    def _pass_config(self):
        for key, value in self.config.items():
            if value[1]:
                try:
                    self.ydl.update_dl_ops(key, int(value[0]))
                except ValueError:
                    self.ydl.update_dl_ops(key, value[0])

    def _download_single_queue(self, progress_callback):
        self._pass_config()
        total = len(self.queue)
        progress_callback.emit(1)
        for ind, url in enumerate(self.queue, start=1):
            self.ydl.download_video(url)
            progress_callback.emit(round(ind / total * 100, 0))
        progress_callback.emit(100)

    def _download_single_video(self, progress_bar=None):
        if self.progress_bar is not None:
            self.progress_bar.hide()
        url = self._get_current_url()
        if url == "https://www.youtube.com/":
            self.bubble.setText("Please select a video")
            self.bubble.show()
        elif not self.ydl.check_if_url_is_playlist(url):
            self._pass_config()
            self.progress_bar = progress_bar
            self.progress_bar.show()
            self.progress_bar.setTextVisible(True)
            self.progress_bar.setFormat("Download starting...")
            self.progress_bar.setValue(0)
            self.worker = Worker(
                self.ydl.download_video,
                url,
                progress=True,
                console=False
            )
            self.worker.signals.progress.connect(self._progress_bar_update)

            self.threadpool.start(self.worker)
        else:
            self.bubble.setText("URL is a playlist")
            self.bubble.show()

    def _download_playlist(self, progress_bar=None):
        if self.progress_bar is not None:
            self.progress_bar.hide()
        url = self._get_current_url()
        if url == "https://www.youtube.com/":
            self.bubble.setText("URL is not a YouTube playlist")
            self.bubble.show()
        elif self.ydl.check_if_url_is_playlist(url):
            self._pass_config()
            self.progress_bar = progress_bar
            self.progress_bar.show()
            self.progress_bar.setTextVisible(True)
            self.progress_bar.setFormat("Download starting...")
            self.progress_bar.setValue(0)
            self.worker = Worker(
                self.ydl.download_playlist,
                url,
                progress=True,
                console=False
            )

            self.worker.signals.progress.connect(self._progress_bar_update)
            self.worker.signals.finished.connect(self._thread_complete)

            self.threadpool.start(self.worker)
        else:
            self.bubble.setText("URL is not a playlist")
            self.bubble.show()

    def _get_current_url(self):
        return self.webview.url().toString().strip()

    def _get_title_of_current_url(self):
        return self.webview.title()

    def _progress_bar_update(self, num):
        """progress_bar_update
        Update progress bar

        Args:
            num (_type_): percentage of the progress bar
        """
        if self.progress_bar is not None:
            self.progress_bar.setTextVisible(False)
            self.progress_bar = format_loading_bar(self.progress_bar, width=self.left_width * 0.35)
            self.progress_bar.setValue(num)
            if num == 100:
                self.progress_bar.setTextVisible(True)
                self.progress_bar.setFormat("Done")

    def back_button_clicked(self):
        if self.settings_widget.width() != 0:
            self.toggle_settings()
        elif self.left_widget.width() != 0:
            self.toggle_downloads()
        else:
            self.webview.back()

    # def onCookieAdded(self, cookie):  # for cookies
    #     for c in self.cookies:
    #         if c.hasSameIdentifier(cookie):
    #             return
    #     self.cookies.append(QNetworkCookie(cookie))
    #     self.toJson()

    # def toJson(self):  # for cookies
    #     cookies_list_info = []
    #     for c in self.cookies:
    #         data = {"name": bytearray(c.name()).decode(), "domain": c.domain(), "value": bytearray(c.value()).decode(),
    #                 "path": c.path(), "expirationDate": c.expirationDate().toString(Qt.ISODate), "secure": c.isSecure(),
    #                 "httponly": c.isHttpOnly()}
    #         cookies_list_info.append(data)

    def clear_cache_clicked(self):
        self.webview.page().profile().clearHttpCache()
        self.webview.page().profile().clearAllVisitedLinks()
        self.webview.page().profile().cookieStore().deleteAllCookies()
        self.webview.setUrl(QUrl(f"https://www.youtube.com/?theme={self.config['theme'][0].lower()}&themeRefresh=1"))
        self.reload_page()
        if self.config['theme'][0] == "Dark":
            self.change_theme(self.config['theme'][0])

    def toggle_dark_mode(self):
        if self.config['theme'][0] == "Dark":
            self.config['theme'] = ("Light", False)
        elif self.config['theme'][0] == "Light":
            self.config['theme'] = ("Dark", False)
        self.change_theme(self.config['theme'][0])
        self.right_widget.dark_mode_yt(self.webview)

    def reload_page(self):
        self.webview.page().triggerAction(QWebEnginePage.ReloadAndBypassCache)

    def change_theme(self, theme: str):
        if self.settings_widget.theme_combo is not None:
            self.settings_widget.theme_combo.setCurrentText(theme)
        with open(f"src/themes/{theme}.qss", "r", encoding="utf-8") as _:
            stylesheet = _.read()
        if f"	color: {self.config['accent'][0].lower()};" not in stylesheet:
            self.config['theme'] = [theme, False]
            self.change_accent(self.config['accent'][0])
        else:
            self.setStyleSheet(stylesheet)

    def change_accent(self, accent: str):
        with open(f"src/themes/{self.config['theme'][0]}.qss", "r", encoding="utf-8") as _:
            stylesheet = _.read()

        for acc in findall(ACCENT, stylesheet):
            if acc not in ("	color: white;", "	color: black;", "	color: transparent;"):
                stylesheet = stylesheet.replace(acc, f"	color: {accent.lower()};")
                break
        with open(f"src/themes/{self.config['theme'][0]}.qss", "w", encoding="utf-8") as _:
            _.write(stylesheet)
        for svg in listdir("src/images/icons"):
            if svg.endswith("_hover.svg"):
                with open(f"src/images/icons/{svg}", "r", encoding="utf-8") as _:
                    svg_data = _.read()
                svg_data = sub(SVG_FILL, f' fill="{accent.lower()}" ', svg_data)
                with open(f"src/images/icons/{svg}", "w", encoding="utf-8") as _:
                    _.write(svg_data)
        self.setStyleSheet(stylesheet)

    def change_download_location(self, location: str):
        pass

    def close(self):
        self.webpage.deleteLater()
        super().close()

if __name__ == "__main__":
    app = QApplication([])
    window = YoutubeDownloader()
    app.exec()
