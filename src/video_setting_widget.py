from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class VideoSettingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("placeholder for video settign widget", self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
