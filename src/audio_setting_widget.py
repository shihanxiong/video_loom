import os
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
from audio_utils import AudioUtils
from file_utils import FileUtils


class AudioSettingWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # state
        self.state = GlobalState()

        # components
        self.main_window = main_window
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
        self.generate_audio_preview_button.clicked.connect(self.generate_audio_preview)
        self.remove_audio_preview_button = QPushButton("Remove preview", self)
        self.remove_audio_preview_button.clicked.connect(self.remove_audio_preview)

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

    def get_audio_preview_filename(self):
        return f"audio_preview_{self.state.data['audio_track_selection'] + 1}.mp3"

    def get_audio_preview(self):
        return FileUtils.get_file_path(self.get_audio_preview_filename())

    def has_audio_preview(self):
        return os.path.exists(self.get_audio_preview())

    def remove_audio_preview(self):
        if self.has_audio_preview():
            os.remove(FileUtils.get_file_path(self.get_audio_preview_filename()))
            self.main_window.status_component.set_and_log_status(
                f"Audio preview deleted for audio track {self.state.data['audio_track_selection'] + 1}"
            )

    def generate_audio_preview(self):
        if len(self.state.data["video_list"]) == 0:
            return

        self.main_window.status_component.set_and_log_status(
            "Generating audio preview, please wait ..."
        )

        video_input = self.state.data["video_list"][
            self.state.data["audio_track_selection"] - 1
        ]
        audio_preview_output = self.get_audio_preview_filename()
        AudioUtils.generate_mp3_from_mp4(video_input, audio_preview_output)

        self.main_window.status_component.set_and_log_status(
            f"Audio preview generated for audio track {self.state.data['audio_track_selection'] + 1}"
        )
