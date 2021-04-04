from PyQt6.QtCore import pyqtSignal, QSize, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QListWidgetItem, QTableWidgetItem, QHeaderView, QMenu
from PyQt6.uic import loadUi

from mock.modals import Mock, Header
from mock.services.mock import MockEnvironmentService
from shared.widget import delete_confirmation


class SwaVanEnvironment(QWidget):
    _mock = Mock()
    saved = pyqtSignal()
    canceled = pyqtSignal()
    selected = pyqtSignal(Mock)

    def __init__(self):
        super(SwaVanEnvironment, self).__init__()
        loadUi("templates/environment.ui", self)
        self.mock_env_list.installEventFilter(self)

        self.mock_env_cancel_btn.clicked.connect(lambda: self.canceled.emit())
        self.mock_env_close_btn.clicked.connect(lambda: self.canceled.emit())
        self.mock_env_add_btn.clicked.connect(self.add_mock_env)
        self.mock_env_save_btn.clicked.connect(self.save)
        self.update_env_list()
        self.mock_env_list.itemSelectionChanged.connect(self.editable)
        self.mock_env_list.doubleClicked.connect(lambda: self.environment_change())

        # Cross Origin Header
        self.add_mock_env_cors_btn.clicked.connect(lambda: self.add_header_row())
        self.mock_env_cors_headers.cellClicked.connect(
            lambda row, col: self.mock_env_cors_headers.removeRow(row) if col == 2 else self.do_nothing())
        self.mock_env_cors_headers.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.mock_env_cors_headers.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.mock_env_cors_headers.horizontalHeader().setMinimumSectionSize(10)
        self.mock_env_cors_headers.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.default_cross_origin_header()

    def __del__(self):
        print('Destructor SwaVanEnvironment')

    def environment_change(self):
        _id = self.mock_env_list.selectedItems()[0].whatsThis()
        _name = self.mock_env_list.selectedItems()[0].text()
        self.selected.emit(Mock(id=_id, name=_name))
        self.canceled.emit()

    def add_mock_env(self):
        self.update_form(Mock())
        self.default_cross_origin_header()

    def update_env_list(self):
        mocks = MockEnvironmentService.load()
        self.mock_env_list.clear()
        for _mock_env in mocks:
            item = QListWidgetItem()
            item.setWhatsThis(_mock_env.id)
            item.setIcon(QIcon("assets/images/icons/environment.ico"))
            item.setText(f"{_mock_env.name}:{_mock_env.port}")
            self.mock_env_list.addItem(item)

    def update_form(self, _mock: Mock = Mock()):
        self._mock = _mock
        self.mock_env_name_input.setText(self._mock.name)
        self.mock_env_port_input.setText(self._mock.port)
        self.mock_env_prefix_input.setText(self._mock.prefix)
        self.mock_env_https_status.setChecked(self._mock.enable_https)
        self.mock_env_cors_status.setChecked(self._mock.enable_cross_origin)

        self.clear_cors_headers()
        self.mock_env_cors_headers.setRowCount(0)
        for _cross_origin in self._mock.cross_origin_allowed_headers:
            self.add_header_row(_cross_origin)

    def clear_cors_headers(self):
        for _cross_origin in range(self.mock_env_cors_headers.rowCount()):
            self.mock_env_cors_headers.removeRow(_cross_origin)

    def editable(self):
        _mocks_env = MockEnvironmentService.load_by_ids([
            _mock_env.whatsThis() for _mock_env in self.mock_env_list.selectedItems()
        ])
        for _mock_env in _mocks_env:
            self.update_form(_mock_env)

    def add_header_row(self, _header: Header = Header()):
        self.mock_env_cors_headers.insertRow(self.mock_env_cors_headers.rowCount())
        row_position = self.mock_env_cors_headers.rowCount()
        self.mock_env_cors_headers.setItem(row_position - 1, 0, QTableWidgetItem(_header.key))
        self.mock_env_cors_headers.setItem(row_position - 1, 1, QTableWidgetItem(_header.value))
        _delete = QTableWidgetItem()
        _delete_icon = QIcon("assets/images/icons/close.ico")
        _delete.setSizeHint(QSize(50, 50))
        _delete.setIcon(_delete_icon)
        self.mock_env_cors_headers.setItem(row_position - 1, 2, _delete)

    def default_cross_origin_header(self):
        for _header in MockEnvironmentService.default_cross_origin_headers():
            self.add_header_row(_header)

    def is_valid(self) -> bool:
        if self.mock_env_name_input.text().strip() or self.mock_env_port_input.text().strip():
            return True
        return False

    def do_nothing(self):
        pass

    def extract(self):
        self._mock.name = self.mock_env_name_input.text()
        self._mock.port = self.mock_env_port_input.text()
        self._mock.prefix = self.mock_env_prefix_input.text()
        self._mock.enable_https = self.mock_env_https_status.isChecked()
        self._mock.enable_cross_origin = self.mock_env_cors_status.isChecked()
        self._mock.cross_origin_allowed_headers = [
            Header(key=self.mock_env_cors_headers.item(i, 0).text(),
                   value=self.mock_env_cors_headers.item(i, 1).text())
            for i in range(self.mock_env_cors_headers.rowCount())]
        return self._mock

    def server_select(self):
        pass

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ContextMenu and source is self.mock_env_list:
            menu = QMenu()
            _copy = menu.addAction(QIcon("assets/images/icons/export.ico"), "Export")
            _remove = menu.addAction(QIcon("assets/images/icons/trash-can.ico"), "Remove")
            if source.itemAt(event.pos()):
                action = menu.exec(event.globalPos())
                _item = source.itemAt(event.pos())
                _id = _item.whatsThis()
                if action == _remove:
                    delete_confirmation(self, _id, self.delete)
                # _id = _item.whatsThis()
                # if action == _copy:
                #     copy_endpoint(endpoint_ids=[_id])
                # elif action == _toggle:
                #     self.toggle_endpoint(_id)
                # elif action == _remove:
                #     self.delete_confirmation(_id)
            return True
        return super().eventFilter(source, event)

    def delete(self, _id: str):
        _status = MockEnvironmentService.remove(_id)
        if _status:
            self.update_env_list()

    def save(self):
        if self.is_valid():
            _mock = self.extract()
            _saved = MockEnvironmentService.save(_mock)
            if _saved:
                self.update_env_list()
                self.add_mock_env()
