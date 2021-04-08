import json
from json.decoder import JSONDecodeError

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from mock.add.endpoint import SwaVanEndpoint
from mock.modals import Endpoint
from mock.services.endpoint import EndpointService
from shared.widgets.builder import template_loader


class SwaVanMockImport(QWidget):
    saved = pyqtSignal()
    canceled = pyqtSignal()

    def __init__(self, ):
        super(SwaVanMockImport, self).__init__()
        template_loader("templates/mock_import.ui", self)
        self.mock_load_json_btn.clicked.connect(self.save)
        self.mock_json_pretty_btn.clicked.connect(self.format_json)
        self.mock_load_json_cancel_btn.clicked.connect(self.canceled)

    def format_json(self):
        self.json_validation_lbl.setText("")
        try:
            _content = self.mock_json_import_input.toPlainText()
            _formatted = json.dumps(json.loads(_content), indent=4)
            self.mock_json_import_input.setText(_formatted)
        except JSONDecodeError as _:
            self.json_validation_lbl.setText("Invalid JSON")
        finally:
            pass

    def validated_endpoints(self):
        try:
            _raw_endpoints = json.loads(self.mock_json_import_input.toPlainText())
            _endpoints = [Endpoint.from_dict(_raw_endpoint) for _raw_endpoint in _raw_endpoints]
            return _endpoints
        except JSONDecodeError as _:
            self.json_validation_lbl.setText("Invalid JSON")
            return []
        finally:
            pass

    def save(self):
        _rows = self.validated_endpoints()
        if len(_rows) > 0:
            _status = EndpointService.save_all(_rows)
            if _status:
                self.saved.emit()
