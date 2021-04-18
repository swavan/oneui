from PyQt5.QtWidgets import QWidget, QHeaderView

from browser_rule.modals import BrowserRule
from shared.widgets.builder import template_loader


class SwaVanBrowserRulePage(QWidget):
    def __init__(self):
        super(SwaVanBrowserRulePage, self).__init__()
        template_loader("templates/browse_rules.ui", self)

    def set_rule(self, _rule: BrowserRule):
        self.browser_rule_name_input.setText()
        self.browser_rule_description_input.setText()
        self.browser_rule_source_combo.setItem()
        self.browser_rule_operator_combo.setItem()
        self.browser_rule_source_input.setText()

        # List of responses
        self.browser_rule_data_source_type_combo.setItem()
        self.browser_link_input.setText()
        self.browser_rule_mock_content.setText()
        self.browser_rule_mock_status_code.setText()
        self.browser_rule_http_method_combo.setItem()
        self.browser_rule_mock_header_btn.clicked.connect(self.add_mock_header)

        # Set Header Table's properties
        self.browser_rule_header_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.browser_rule_header_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.browser_rule_header_table.horizontalHeader().setSectionResizeMode(2,
                                                                               QHeaderView.ResizeMode.ResizeToContents)

        self.browser_rule_mock_filters_btn.clicked.connect(self.add_browser_rule_filter)
        # Set Header Table's properties
        self.browser_rule_filtes_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.browser_rule_filtes_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.browser_rule_filtes_table.horizontalHeader().setSectionResizeMode(2,
                                                                               QHeaderView.ResizeMode.ResizeToContents)

        self.browser_rule_given_name.setText()
        self.is_enabled_checkbox.setChecked(True)

    def add_mock_header(self):
        # self.browser_rule_header_table.set
        pass

    def add_browser_rule_filter(self):
        # self.browser_rule_filtes_table
        pass
