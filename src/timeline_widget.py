from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from global_state import GlobalState


class TimelineWidget(QWidget):
    def __init__(self):
        super().__init__()

        # state
        self.state = GlobalState()

        # components
        self.timeline_label = QLabel("Timeline", self)
        self.timeline_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.timeline_text = QTextEdit()
        self.timeline_text.setPlaceholderText(
            """Enter timeline here, each line stands for a segment. For example:
2, 0:00:00, 0:00:10  # trims video #2 from 0:00:00 to 0:00:10
1, 0:00:10, 0:01:05  # trims video #1 from 0:00:10 to 0:01:05"""
        )
        self.timeline_text.textChanged.connect(self.on_text_changed)

        # component layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.timeline_label)
        self.layout.addWidget(self.timeline_text)

    def on_text_changed(self):
        timeline_text = self.timeline_text.toPlainText()
        self.state.data["timeline"] = timeline_text
