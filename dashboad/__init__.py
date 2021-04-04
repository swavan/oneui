from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.uic import loadUi

from mock.page import SwaVanMockPage


class SwaVanDashboard(QWidget):
    def __init__(self):
        super(SwaVanDashboard, self).__init__()
        loadUi("templates/swavan.ui", self)

        mock_page = SwaVanMockPage()
        self.features.addWidget(mock_page)


class SwaVanMainWindow(QMainWindow):
    previous_pos = None
    _drag_active = False

    def __init__(self, *args, **kwargs):
        super(SwaVanMainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("assets/images/logo/swavan_one_ui.png"))
        self.setContentsMargins(0, 0, 0, 0)
        _window = SwaVanDashboard()
        self.setCentralWidget(_window)
        self.setWindowTitle("SwaVan")
