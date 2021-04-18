from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow

from browser_rule.page import SwaVanBrowserRulePage
from mock.page import SwaVanMockPage
from shared.widgets.builder import template_loader, full_path


class SwaVanDashboard(QWidget):
    def __init__(self):
        super(SwaVanDashboard, self).__init__()
        template_loader("templates/swavan.ui", self)
        # _page = SwaVanBrowserRulePage()
        _page = SwaVanMockPage()
        self.features.addWidget(_page)


class SwaVanMainWindow(QMainWindow):
    previous_pos = None
    _drag_active = False

    def __init__(self, *args, **kwargs):
        super(SwaVanMainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(full_path("assets/images/logo/swavan_one_ui.png")))
        self.setContentsMargins(0, 0, 0, 0)
        _window = SwaVanDashboard()
        self.setCentralWidget(_window)
        self.setWindowTitle("SwaVan")
