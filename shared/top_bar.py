from PyQt5.QtWidgets import QWidget

from shared.widgets.builder import template_loader


class SwaVanTopBar(QWidget):

    def __init__(self,):
        super(SwaVanTopBar, self).__init__()
        template_loader("templates/top_bar.ui", self)
        self.close_window_btn.clicked.connect(self.shutdown)

    def shutdown(self):
        self.close()
        QApplication.quit()