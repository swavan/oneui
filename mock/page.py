from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QDockWidget, QTextEdit

from mock.add import SwaVanMockImport
from mock.add.endpoint import SwaVanEndpoint
from mock.environment import SwaVanEnvironment
from mock.modals import Mock
from mock.servers.config import ServerTypes
from mock.servers.server import SwaVanMockServerService
from mock.services.endpoint import EndpointService
from mock.services.mock import MockEnvironmentService
from mock.view import SwaVanMockEndpoints
from shared.recorder import SwaVanLogRecorder
from shared.widgets.builder import template_loader, full_path
from stores.cache import SwaVanCache


class SwaVanMockPage(QWidget):
    _animation = None
    environment_changed = pyqtSignal()

    def __init__(self):
        super(SwaVanMockPage, self).__init__()
        template_loader("templates/mock.ui", self)
        _last = MockEnvironmentService.last_seen()
        self.mock_server_selected_btn.setText(f" {_last.name} : {_last.port} ")
        SwaVanCache.set_selected_env(_last.id)

        _endpoints = SwaVanMockEndpoints()
        _endpoints.setObjectName("SwaVanMockEndpoints")
        self.endpoints_placeholder.addWidget(_endpoints)
        self.environment_changed.connect(lambda: _endpoints.update_view())

        _endpoint = SwaVanEndpoint()
        _endpoint.setObjectName("SwaVanEndpoint")

        _endpoint.saved.connect(_endpoints.update_view)
        self.mock_content_view.addWidget(_endpoint)

        _endpoints.edit.connect(lambda x: _endpoint.update_view(x))
        self.add_mock_btn.clicked.connect(lambda: _endpoint.update_view())

        self.import_mock_btn.clicked.connect(self.import_mocks)
        self.mock_toggle_endpoints_btn.clicked.connect(self.toggle_view)

        self.log_view_btn.clicked.connect(self.create_log_view)
        self.mock_server_selected_btn.clicked.connect(self.environment_settings)

        self.server_status_btn.clicked.connect(self.toggle_endpoint)

    def toggle_endpoint(self):
        is_running = SwaVanMockServerService.is_running(SwaVanCache.get_selected_env())
        if is_running:
            SwaVanMockServerService.stop(SwaVanCache.get_selected_env())
            self.play_icon_update(not is_running)
        else:
            _mock = MockEnvironmentService.load_by_id(SwaVanCache.get_selected_env())
            if _mock:
                _endpoints = EndpointService.load_by_parent(_mock.id)
                if _endpoints:
                    _mock.endpoints = _endpoints
                SwaVanMockServerService.start(_mock, ServerTypes.REST)
                self.play_icon_update(not is_running)
    
    def play_icon_update(self, is_running: bool):
        _icon = QIcon(full_path(f"assets/images/icons/{'play' if not is_running else 'stop'}.ico"))
        self.server_status_btn.setIcon(_icon)

    def toggle_view(self):
        _width = self.endpointViewPanel.width()
        expected_width = 0
        if _width == 0:
            expected_width = 230
        self._animation = QPropertyAnimation(self.endpointViewPanel, b"maximumWidth")
        self._animation.setDuration(250)
        self._animation.setStartValue(_width)
        self._animation.setEndValue(expected_width)
        self._animation.start()

    def import_mocks(self):
        _mockImport = SwaVanMockImport()
        _endpoints = self.findChild(SwaVanMockEndpoints, "SwaVanMockEndpoints")
        _mockImport.saved.connect(_endpoints.update_view)
        self._dialog_handler(_mockImport)

    def environment_settings(self):
        _env = SwaVanEnvironment()
        _env.selected.connect(lambda x: self.change_selected_env(x))
        self._dialog_handler(_env)

    def change_selected_env(self, _env: Mock):
        SwaVanCache.set_selected_env(_env.id)
        self.mock_server_selected_btn.setText(_env.name)
        self.environment_changed.emit()
        is_running = SwaVanMockServerService.is_running(SwaVanCache.get_selected_env())
        self.play_icon_update(is_running)

    def create_log_view(self):
        _dock = QDockWidget("Log", self)
        _dock.setFloating(True)
        _view = QTextEdit()
        _dock.setWindowModality(Qt.WindowModality.NonModal)
        for row in SwaVanLogRecorder.reading_log():
            _pre = _view.toPlainText()
            _view.setPlainText(f"{_pre}\n{row}")

        _view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        _view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        _dock.setWidget(_view)
        self.mock_right_size.addWidget(_dock)

    def _dialog_handler(self, _widget: QWidget):
        _dialog = QDialog(self)

        _widget.saved.connect(_dialog.close)
        _widget.canceled.connect(_dialog.close)

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.addWidget(_widget)

        _dialog.setWindowModality(Qt.WindowModality.WindowModal)
        _dialog.setLayout(_layout)

        _parent_size = self.sizeHint()
        _modal_size = QSize(_parent_size.width() - 100, _parent_size.height() - 100)

        _dialog.setFixedSize(_modal_size)
        _dialog.show()
