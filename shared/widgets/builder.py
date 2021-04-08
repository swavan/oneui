import os

from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


def template_loader(filename: str, _widget: QWidget) -> None:
    root_dir = os.path.abspath(os.curdir)
    ui = os.path.join(root_dir, filename)
    loadUi(ui, _widget)


def full_path(file_path: str) -> str:
    root_dir = os.path.abspath(os.curdir)
    return os.path.join(root_dir, file_path)