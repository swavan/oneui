import os

from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QListWidgetItem, QMenu
from PyQt6.uic import loadUi

from mock.modals import Endpoint
from mock.services.endpoint import EndpointService
from shared.helper import copy_endpoint
from shared.widget import delete_confirmation
from shared.widgets.builder import template_loader, full_path
from stores.cache import SwaVanCache


class SwaVanMockEndpoints(QWidget):
    edit = pyqtSignal(Endpoint)

    def __init__(self):
        super(SwaVanMockEndpoints, self).__init__()
        template_loader("templates/endpoints.ui", self)
        self.mock_endpoints.installEventFilter(self)
        self.mock_endpoints.itemDoubleClicked.connect(self.selected_item)
        self.update_view()

    def selected_item(self):
        _items = self.mock_endpoints.selectedItems()
        _endpoints = EndpointService.load_by_ids([_item.whatsThis() for _item in _items])
        if _endpoints and len(_endpoints) > 0:
            self.edit.emit(_endpoints[0])

    def update_view(self):
        self.mock_endpoints.clear()
        _endpoints = EndpointService.load_by_parent(SwaVanCache.get_selected_env())
        _endpoints.sort(key=lambda x: x.created_at)
        if SwaVanCache.get_selected_env():
            for row in _endpoints:
                item = QListWidgetItem(row.url)
                item.setWhatsThis(row.id)
                icon = QIcon(full_path(f"assets/images/icons/{'sad' if not row.is_active else row.http_method.lower()}.ico"))
                item.setToolTip(f"""<b>{row.http_method.title()}</b> {row.url} { 'is disabled' if not row.is_active else ''}""")
                item.setIcon(icon)
                self.mock_endpoints.addItem(item)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ContextMenu and source is self.mock_endpoints:
            menu = QMenu()
            _copy = menu.addAction(QIcon(full_path("assets/images/icons/copy.ico")), "Copy")
            _toggle = menu.addAction(QIcon(full_path("assets/images/icons/toggle.ico")), "Toggle")
            _remove = menu.addAction(QIcon(full_path("assets/images/icons/trash-can.ico")), "Remove")

            if source.itemAt(event.pos()):
                action = menu.exec(event.globalPos())
                _item = source.itemAt(event.pos())
                _id = _item.whatsThis()
                if action == _copy:
                    copy_endpoint(endpoint_ids=[_id])
                elif action == _toggle:
                    self.toggle_endpoint(_id)
                elif action == _remove:
                    delete_confirmation(self, _id, self.delete)
            return True
        return super().eventFilter(source, event)

    def delete(self, _id: str):
        EndpointService.remove(_id)
        self.update_view()

    def toggle_endpoint(self, _id: str):
        status = EndpointService.toggle_state([_id])
        if status:
            self.update_view()
