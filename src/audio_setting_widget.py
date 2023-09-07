from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
)
from PyQt6.QtCore import Qt
from global_state import GlobalState


class AudioSettingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # state
        self.state = GlobalState()

        # components
        self.audio_setting_label = QLabel("Audio Settings", self)
        self.audio_setting_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.audio_track_label = QLabel("audio track:", self)
        self.audio_track_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.audio_track_label.setContentsMargins(0, 3, 0, 0)
        self.audio_track_selection = QComboBox()
        self.audio_track_selection.addItems(["1", "2", "3", "4"])
        self.audio_track_selection.activated.connect(
            self.on_audio_track_selection_activated
        )
        self.generate_audio_preview_button = QPushButton("Generate preview", self)
        self.generate_audio_preview_button.setEnabled(False)
        self.remove_audio_preview_button = QPushButton("Remove preview", self)
        self.remove_audio_preview_button.setEnabled(False)

        # component layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.audio_setting_label)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.audio_track_label)
        sub_layout.addWidget(self.audio_track_selection)
        sub_layout.addWidget(self.generate_audio_preview_button)
        sub_layout.addWidget(self.remove_audio_preview_button)
        main_layout.addLayout(sub_layout)

    def on_audio_track_selection_activated(self):
        selected_value = int(self.audio_track_selection.currentText()) - 1
        self.state.data["audio_track_selection"] = selected_value
