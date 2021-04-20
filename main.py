import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from dashboad import SwaVanMainWindow
from shared.recorder import SwaVanLogRecorder
from shared.widgets.builder import full_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("SwaVan")
    app.setApplicationName("SwaVan")
    app.setDesktopFileName("SwaVan")

    app.setWindowIcon(QIcon(full_path("assets/images/logo/swavan_one_ui.icns")))
    with open(full_path("assets/style/dark.qss"), 'r') as file:
        qss = file.read()
        app.setStyleSheet(qss)
        if os.path.exists(full_path("data/logs/swavan.log")):
            open(full_path("data/logs/swavan.log"), 'w').close()

    widget = SwaVanMainWindow()
    widget.show()
    SwaVanLogRecorder.init()
    sys.exit(app.exec())
