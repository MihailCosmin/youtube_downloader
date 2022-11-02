from datetime import datetime

from PySide6 import QtWebEngineWidgets
from PySide6 import QtWebEngineCore

from PySide6.QtCore import QUrl

from PySide6 import QtWidgets
from PySide6.QtCore import QByteArray

from PySide6.QtWebEngineCore import QWebEngineHttpRequest
from PySide6.QtWebEngineCore import QWebEnginePage

from adblockparser import AdblockRules

with open("src/ytb/easylist.txt", "r", encoding="utf-8") as _:
    raw_rules = _.readlines()
    rules = AdblockRules(raw_rules)

class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        current_time = datetime.now().strftime("%H:%M:%S")
        if "watch?" in url and f"theme={self.parent.config['theme'][0].lower()}" not in url and "reel" not in url:
            url = url.replace("?", f"?theme={self.parent.config['theme'][0].lower()}&")
            self.parent.webview.setUrl(QUrl(url))
            # TODO: Check how to apply theme to other pages: shorts, home, playlists?? etc
        elif url == "https://www.youtube.com/":
            self.parent.webview.setUrl(QUrl(url[:-1] + "?theme=" + self.parent.config['theme'][0].lower()))
        elif rules.should_block(url):
            # print(f"1 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "adformat" in url:
            # print(f"2 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "ads" in url:
            # print(f"3 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "ad.doubleclick" in url:
            # print(f"4 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return

class RightWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.right_layout = QtWidgets.QGridLayout()
        self.setLayout(self.right_layout)
        self.right_layout.setContentsMargins(10, 0, 0, 0)

        self.setMinimumWidth(self.parent.right_width)
        self.setMaximumWidth(self.parent.right_width + self.parent.left_width)
        self.parent.webview = self._youtube_browser_widget()
        self.parent.webview.setObjectName = u"webview"
        self.right_layout.addWidget(self.parent.webview)

    def _youtube_browser_widget(self):
        browser = QtWebEngineWidgets.QWebEngineView()
        self.parent._profile = QtWebEngineCore.QWebEngineProfile("F_Youtube", browser)  # Fuck Youtube = F_Youtube
        self.parent._profile.setPersistentCookiesPolicy(QtWebEngineCore.QWebEngineProfile.ForcePersistentCookies)

        # self.parent.cookie_store = self.parent._profile.cookieStore()  # for cookies
        # self.parent.cookie_store.cookieAdded.connect(self.parent.onCookieAdded)  # for cookies
        # self.parent.cookies = []  # for cookies

        self.parent.webpage = QWebEnginePage(self.parent._profile, browser)
        browser.setPage(self.parent.webpage)

        self._adblock()
        self.dark_mode_yt(browser)

        return browser

    def dark_mode_yt(self, browser):
        url = QWebEngineHttpRequest()
        url.setHeader(
            QByteArray(b'cookie'),
            QByteArray('CONSENT=YES+,\
                       CONSISTENCY=APAR8ns3uxo7ct7gBg55K_ihesLT02MnRwMLB6PgW3oVmKqoUI1MEpLBsE0g49xnK_Tb,\
                       GPS=0,\
                       PREF=f4=4000000&tz=Europe.Berlin&f6=400,\
                       SOCS=CAISFggDEgk0NzUzMDQ3NzEaBWVuLUdCIAEaBgiAqKmZBg,\
                       '.replace("                       ", "").encode())
        )
        url.setUrl("https://www.youtube.com")
        browser.load(url)
        url.setUrl(f"https://www.youtube.com/?theme={self.parent.config['theme'][0].lower()}&themeRefresh=1")
        browser.load(url)
        
        # browser.load(QtCore.QUrl("https://www.youtube.com/?theme=dark&themeRefresh=1"))
        # browser.load(QtCore.QUrl("https://www.yewtu.be"))

    def _adblock(self):
        # TODO: Make ads traffic filter work
        # https://github.com/qutebrowser/qutebrowser/issues/6480
        # https://bugreports.qt.io/browse/QTBUG-51185
        # https://forum.qt.io/topic/131378/enabling-extensions-on-pyqt
        self.parent._interceptor = WebEngineUrlRequestInterceptor(parent=self.parent)
        self.parent._profile.setUrlRequestInterceptor(self.parent._interceptor)
