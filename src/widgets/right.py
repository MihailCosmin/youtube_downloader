from datetime import datetime

from PySide6 import QtWebEngineWidgets
from PySide6 import QtWebEngineCore

from PySide6 import QtWidgets
from PySide6.QtCore import QByteArray

from PySide6.QtWebEngineCore import QWebEngineHttpRequest
from PySide6.QtWebEngineCore import QWebEnginePage

from adblockparser import AdblockRules

with open("easylist_clean.txt", "r", encoding="utf-8") as _:
    raw_rules = _.readlines()
    rules = AdblockRules(raw_rules)

class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        with open("accepted_urls.txt", "w", encoding="utf-8") as _:
            _.write("")

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        current_time = datetime.now().strftime("%H:%M:%S")
        if rules.should_block(url):
            print(f"1 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "adformat" in url:
            print(f"2 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "ads" in url:
            print(f"3 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        elif "ad.doubleclick" in url:
            print(f"4 - {current_time} - block::::::::::::::::::::::", url)
            info.block(True)
            return
        else:
            with open("accepted_urls.txt", "a", encoding="utf-8") as _:
                _.write(f"{current_time} - {url}\n")

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
        self.parent._profile = QtWebEngineCore.QWebEngineProfile("F_Youtube", browser)
        self.parent._profile.setPersistentCookiesPolicy(QtWebEngineCore.QWebEngineProfile.ForcePersistentCookies)
        self.parent.webpage = QWebEnginePage(self.parent._profile, browser)
        browser.setPage(self.parent.webpage)

        self._adblock()
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
        url.setUrl("https://www.youtube.com/?theme=dark&themeRefresh=1")
        browser.load(url)
        # browser.load(QtCore.QUrl("https://www.youtube.com/?theme=dark&themeRefresh=1"))
        # browser.load(QtCore.QUrl("https://www.yewtu.be"))
        return browser

    def _adblock(self):
        # TODO: Make ads traffic filter work
        # https://github.com/qutebrowser/qutebrowser/issues/6480
        # https://bugreports.qt.io/browse/QTBUG-51185
        # https://forum.qt.io/topic/131378/enabling-extensions-on-pyqt
        self.parent._interceptor = WebEngineUrlRequestInterceptor(parent=self.parent)
        self.parent._profile.setUrlRequestInterceptor(self.parent._interceptor)
