from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class VideoIntroOutroWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("placeholder for intro/outro widget", self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
