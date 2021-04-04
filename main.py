import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from dashboad import SwaVanMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("SwaVan")
    app.setApplicationName("SwaVan")
    app.setDesktopFileName("SwaVan")

    app.setWindowIcon(QIcon("assets/images/logo/swavan_one_ui.png"))
    with open("assets/style/dark.qss", 'r') as file:
        qss = file.read()
        app.setStyleSheet(qss)

    widget = SwaVanMainWindow()
    widget.show()
    sys.exit(app.exec())
