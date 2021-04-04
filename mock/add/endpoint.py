import copy
import uuid
from typing import List

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QFileDialog, QDialog, QVBoxLayout
from PyQt6.uic import loadUi

from mock.modals import Endpoint, Response, Header, Rule
from mock.services.endpoint import EndpointService
from shared.codes import HTTP_METHODS, FILTER_BY_OPTIONS, OPERATORS
from shared.helper import code_to_text, text_to_code
from shared.widgets.editor import SwaVanCodeEditor
from stores.cache import SwaVanCache


class SwaVanEndpoint(QWidget):
    saved = pyqtSignal()
    _response_selected = 0
    _store: Endpoint

    def __init__(self, **kwargs):
        super(SwaVanEndpoint, self).__init__()
        self._store = EndpointService.reset()
        if kwargs.get('data'):
            self._store = kwargs.get('data')

        loadUi("templates/endpoint_identifier.ui", self)

        self.body_input = SwaVanCodeEditor()
        self.mock_data_editor_layout.addWidget(self.body_input)

        self.endpoint_btn.clicked.connect(lambda: self.change_page(0))
        self.headers_btn.clicked.connect(lambda: self.change_page(1))
        self.status_btn.clicked.connect(lambda: self.change_page(2))
        self.rules_btn.clicked.connect(lambda: self.change_page(3))

        self.add_btn.clicked.connect(self.add_response)
        self.duplicate_response_btn.clicked.connect(self.duplicate_response)
        self.next_btn.clicked.connect(self.next_response)
        self.previous_btn.clicked.connect(self.prev_response)
        self.delete_btn.clicked.connect(self.delete_endpoint)
        self.save_btn.clicked.connect(self.save)
        self.redirect_response_modify.clicked.connect(lambda: self.code_editor("modifier"))
        self.advaance_rule_codes_btn.clicked.connect(lambda: self.code_editor("filter_by"))

        self.http_method_combo.addItems(map(lambda x: x.title(), HTTP_METHODS.values()))
        self.filter_by_combo.addItems(FILTER_BY_OPTIONS.values())
        self.rule_operator_combo.addItems(OPERATORS.values())
        self.set_endpoint(self._store)

        self.header_tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.header_tbl.clicked.connect(lambda x: self.header_row_clicked(x))

        self.add_header_btn.clicked.connect(lambda: self.add_header())

        # Rule table
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.mock_rule_tbl.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.mock_rule_tbl.clicked.connect(lambda x: self.rule_row_clicked(x))

        # Delay validation
        self.delay_input.setValidator(QIntValidator())

        # Upload file
        self.upload_btn.clicked.connect(self.upload)

        # Status code validator
        self.status_code_input.setValidator(QIntValidator())

        # create new rule
        self.rule_add_btn.clicked.connect(self.add_rule)
        self.cmb_rules_connector.addItems(['And', 'Or'])

        # Default Selected button
        self.change_page(0)

        # change response order
        self.move_up_btn.clicked.connect(self.move_up)
        self.move_down_btn.clicked.connect(self.move_down)

    def move_up(self):
        if len(self._store.responses) > self._response_selected+1:
            self.update_response()
            self._store.responses[self._response_selected], self._store.responses[self._response_selected + 1] = [
                self._store.responses[self._response_selected + 1], self._store.responses[self._response_selected]
            ]
            self._response_selected = self._response_selected + 1
            self.update_position_info()

    def update_position_info(self):
        self.response_page_lbl.setText(f"{self._response_selected + 1} of {len(self._store.responses)}")

    def move_down(self):
        if self._response_selected > 0:
            self.update_response()
            self._store.responses[self._response_selected], self._store.responses[self._response_selected - 1] = [
                self._store.responses[self._response_selected - 1], self._store.responses[self._response_selected]
            ]
            self._response_selected = self._response_selected - 1
            self.update_position_info()

    def change_page(self, index: int):
        self.update_button_check_state()
        if index == 0:
            self.endpoint_btn.setChecked(True)
        elif index == 1:
            self.headers_btn.setChecked(True)
        elif index == 2:
            self.status_btn.setChecked(True)
        elif index == 3:
            self.rules_btn.setChecked(True)

        self.endpoints.setCurrentIndex(index)

    def update_button_check_state(self):
        self.endpoint_btn.setChecked(False)
        self.headers_btn.setChecked(False)
        self.status_btn.setChecked(False)
        self.rules_btn.setChecked(False)

    def upload(self):
        _file = QFileDialog.getOpenFileName(self, 'Open File', '.')
        _name, _ = _file
        self.file_url_input.setText(_name)

    def add_response(self):
        self.update_response()
        self._store.responses.append(EndpointService.response_reset())
        self.next_response()

    def duplicate_response(self):
        self.update_response()
        _response = copy.copy(self._store.responses[self._response_selected])
        _response.id = str(uuid.uuid4())
        self._store.responses.append(_response)
        self.next_response()

    def next_response(self):
        if len(self._store.responses) > self._response_selected + 1:
            self.update_response()
            self._response_selected = self._response_selected + 1
            self.reset()
            self.set_response(self._store.responses[self._response_selected])
            self.response_page_lbl.setText(f"{self._response_selected + 1} of {len(self._store.responses)}")

    def prev_response(self):
        self.update_response()
        if self._response_selected > 0:
            self._response_selected = self._response_selected - 1
            self.reset()
            self.set_response(self._store.responses[self._response_selected])
            self.response_page_lbl.setText(f"{self._response_selected + 1} of {len(self._store.responses)}")

    def reset(self):
        self.header_tbl.setRowCount(0)
        self.mock_rule_tbl.setRowCount(0)

    def delete_endpoint(self):
        if len(self._store.responses) > 1:
            self.prev_response()
            self._store.responses.pop(self._response_selected)
            self.response_page_lbl.setText(f"{self._response_selected + 1} of {len(self._store.responses)}")

    def set_endpoint(self, _endpoint: Endpoint):
        self._response_selected = 0
        self.http_method_combo.setCurrentText(_endpoint.http_method)
        self.url_input.setText(_endpoint.url)
        self.delay_input.setText(str(_endpoint.delay))
        self.set_response(_endpoint.responses[self._response_selected])
        self.response_page_lbl.setText(f"{self._response_selected + 1} of {len(self._store.responses)}")

    def set_response(self, _response: Response):
        self.file_url_input.setText(_response.content_path)
        self.body_input.text = _response.content
        self.redirect_input.setText(_response.redirect)
        self.isEndpointActive.setChecked(_response.is_active)
        self.status_code_input.setText(str(_response.status))
        self.set_headers(_response.headers)
        self.cmb_rules_connector.setCurrentText(_response.connector)
        self.set_rules(_response.rules)

    def set_headers(self, _headers: List[Header]):
        self.header_tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header_tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for _header in _headers:
            self.add_header(_header)

    def add_rule(self):
        if self.filter_by_combo.currentText() \
                and self.field_input.text() \
                and self.rule_operator_combo.currentText():
            self.add_mock_rule(Rule(
                filter_by=self.filter_by_combo.currentText(),
                field=self.field_input.text(),
                operator=self.rule_operator_combo.currentText(),
                value=self.rule_value_input.text()
            ))

    def set_rules(self, _rules: List[Rule]):
        for _rule in _rules:
            self.add_mock_rule(_rule)

    def header_row_clicked(self, _select):
        if _select.column() == 2:
            self.header_tbl.removeRow(_select.row())

    def add_header(self, _header: Header = Header()):
        self.header_tbl.insertRow(self.header_tbl.rowCount())
        row_position = self.header_tbl.rowCount() - 1
        self.header_tbl.setItem(row_position, 0, QTableWidgetItem(_header.key))
        self.header_tbl.setItem(row_position, 1, QTableWidgetItem(_header.value))
        delete_text = QTableWidgetItem()
        delete_text.setIcon(QIcon("assets/images/icons/close.ico"))
        self.header_tbl.setItem(row_position, 2, delete_text)

    def rule_row_clicked(self, _select):
        if _select.column() == 5:
            self.mock_rule_tbl.removeRow(_select.row())
        if _select.column() == 4:
            _pre = self.mock_rule_tbl.item(_select.row(), 4).text()
            self.mock_rule_tbl.setItem(_select.row(), 4, QTableWidgetItem("&&" if _pre == "Or" else "Or"))

    def add_mock_rule(self, _rule: Rule = Rule()):
        self.mock_rule_tbl.insertRow(self.mock_rule_tbl.rowCount())
        row_position = self.mock_rule_tbl.rowCount() - 1
        self.mock_rule_tbl.setItem(row_position, 0, QTableWidgetItem(_rule.filter_by))
        self.mock_rule_tbl.setItem(row_position, 1, QTableWidgetItem(_rule.field))
        self.mock_rule_tbl.setItem(row_position, 2, QTableWidgetItem(_rule.operator))
        self.mock_rule_tbl.setItem(row_position, 3, QTableWidgetItem(_rule.value))
        self.mock_rule_tbl.setItem(row_position, 4, QTableWidgetItem("x"))

    def update_response(self):
        _rules = [Rule(
            filter_by=self.mock_rule_tbl.item(i, 0).text(),
            field=self.mock_rule_tbl.item(i, 1).text(),
            operator=self.mock_rule_tbl.item(i, 2).text(),
            value=self.mock_rule_tbl.item(i, 3).text(),
        ) for i in range(self.mock_rule_tbl.rowCount())]

        _headers = [Header(
            key=self.header_tbl.item(i, 0).text(),
            value=self.header_tbl.item(i, 1).text()) for i in range(self.header_tbl.rowCount())]

        self._store.responses[self._response_selected].content_path = self.file_url_input.text()
        self._store.responses[self._response_selected].content = self.body_input.text
        self._store.responses[self._response_selected].redirect = self.redirect_input.text()
        self._store.responses[self._response_selected].is_active = self.isEndpointActive.isChecked()
        self._store.responses[self._response_selected].status = int(self.status_code_input.text())
        self._store.responses[self._response_selected].headers = _headers
        self._store.responses[self._response_selected].connector = self.cmb_rules_connector.currentText()
        self._store.responses[self._response_selected].rules = _rules

    def update_endpoint(self):
        self._store.http_method = self.http_method_combo.currentText()
        self._store.url = self.url_input.text()
        self._store.delay = int(self.delay_input.text() or 0)

    def update_view(self, endpoint: Endpoint = EndpointService.reset()):
        self.reset()
        self._store = endpoint
        self.set_endpoint(endpoint)

    def set_modifier(self, codes: str):
        self._store.responses[self._response_selected].modifier = text_to_code(codes)

    def get_modifier(self):
        return code_to_text(self._store.responses[self._response_selected].modifier)

    def set_filter_by(self, codes: str):
        self._store.responses[self._response_selected].filter_by = text_to_code(codes)

    def get_filter_by(self):
        return code_to_text(self._store.responses[self._response_selected].filter_by)

    def code_editor(self, editor_associated: str):
        _editor = SwaVanCodeEditor()
        _editor.form_view()
        _editor.update_lexer("python")
        _dialog = QDialog(self)
        if editor_associated == "modifier":
            _editor.text = self.get_modifier()
            _editor.editor_save.connect(lambda x: self.set_modifier(x))
            if not _editor.text:
                _editor.text = EndpointService.default_swavan_response()
        elif editor_associated == "filter_by":
            _editor.text = self.get_filter_by()
            _editor.editor_save.connect(lambda x: self.set_filter_by(x))
            if not _editor.text:
                _editor.text = EndpointService.default_swavan_rule()
        _editor.editor_close.connect(lambda: _dialog.close())
        _editor.editor_save.connect(lambda _: _dialog.close())
        _layout = QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.addWidget(_editor)

        _dialog.setWindowModality(Qt.WindowModality.WindowModal)
        _dialog.setLayout(_layout)
        _parent_size = self.sizeHint()
        _modal_size = QSize(_parent_size.width(), _parent_size.height())

        _dialog.setFixedSize(_modal_size)
        _dialog.show()

    def save(self):
        self.update_endpoint()
        self.update_response()
        self._store.pid = SwaVanCache.get_selected_env()
        is_empty = self._store.http_method and self._store.url
        is_duplicate = EndpointService.is_endpoint_duplicate(
            self._store.url,
            self._store.http_method)

        if is_empty and not is_duplicate:
            status = EndpointService.save(self._store)
            if status:
                self._response_selected = 0
                self.update_view(EndpointService.reset())
                self.saved.emit()
