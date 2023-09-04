from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("placeholder for status widget", self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
