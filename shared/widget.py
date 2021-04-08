from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QPushButton

from shared.helper import do_nothing
from shared.widgets.builder import full_path


def delete_confirmation(parent, _id: str, action: Callable):
    msg = QMessageBox()
    msg.setText("Are you sure, you want to remove ?")
    msg.setStyleSheet('''
        background-color: #1d251c;
        color: #bdc0bd;
    ''')
    msg.setParent(parent)
    msg.setWindowModality(Qt.WindowModality.WindowModal)

    style = '''
    margin-top: 20px;
    border: none;
    '''
    yes_btn = QPushButton("  Yes")
    yes_btn.setIcon(QIcon(full_path("assets/images/icons/trash-can.ico")))
    yes_btn.setStyleSheet(style)

    no_btn = QPushButton("  Cancel")
    no_btn.setStyleSheet(style)
    no_btn.setIcon(QIcon(full_path("assets/images/icons/cancel.ico")))

    yes_btn.setDefault(True)

    msg.addButton(no_btn, msg.ButtonRole.NoRole)
    msg.addButton(yes_btn, msg.ButtonRole.YesRole)

    msg.buttonClicked.connect(lambda x: action(_id) if x.text().lower().strip() == "yes" else do_nothing())
    msg.exec()
