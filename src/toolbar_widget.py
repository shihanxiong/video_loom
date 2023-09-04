from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QCoreApplication


class ToolbarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.generate_button = QPushButton("Generate Video", self)
        self.generate_button.setEnabled(False)  # TODO
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(QCoreApplication.quit)

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.quit_button)
