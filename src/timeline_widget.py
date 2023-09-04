from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class TimelineWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("placeholder for timeline widget", self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
