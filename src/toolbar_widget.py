from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class ToolbarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("placeholder for toolbar widget", self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
