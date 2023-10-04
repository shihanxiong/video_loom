from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
)
from PyQt6.QtCore import Qt
from global_state import GlobalState


class VideoSettingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # state
        self.state = GlobalState()

        # components
        self.video_setting_label = QLabel("Video Settings", self)
        self.video_setting_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ffmpeg_preset_label = QLabel("process speed:", self)
        self.ffmpeg_preset_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ffmpeg_preset_label.setContentsMargins(0, 3, 0, 0)
        self.ffmpeg_preset_selection = QComboBox()
        self.ffmpeg_preset_selection.addItems(
            [
                "ultrafast",
                "superfast",
                "veryfast",
                "faster",
                "fast",
                "medium",
                "slow",
                "slower",
                "veryslow",
            ]
        )

        # component layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_setting_label)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.ffmpeg_preset_label)
        sub_layout.addWidget(self.ffmpeg_preset_selection)
        sub_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(sub_layout)

    def on_ffmpeg_preset_selection_activated(self):
        selected_value = self.ffmpeg_preset_selection.currentText()
        self.state.data["ffmpeg_preset_value"] = selected_value
