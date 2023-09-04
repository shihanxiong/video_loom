from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
import logging


class StatusWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # components
        self.main_window = main_window

    def set_and_log_status(self, status):
        self.main_window.statusBar().showMessage(status)
        logging.info(status)
