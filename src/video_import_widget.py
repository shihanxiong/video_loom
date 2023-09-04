from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog
from global_state import GlobalState


class VideoImportWidget(QWidget):
    _TITLE_VIEW_VIDEO_LIST = "View Videos List"
    _BUTTON_TEXT_PLAY_ALL_VIDEOS = "Play all videos"
    _BUTTON_TEXT_PAUSE_ALL_VIDEOS = "Pause all videos"

    def __init__(self, main_window):
        super().__init__()

        # state
        self.state = GlobalState()

        # components
        self.main_window = main_window
        self.video_import_button = QPushButton("Import videos", self)
        self.video_import_button.clicked.connect(self.import_videos)
        self.view_video_list_button = QPushButton(
            f"View video list ({len(self.state.data['video_list'])} of 4)", self
        )
        self.play_pause_videos_button = QPushButton(
            self._BUTTON_TEXT_PLAY_ALL_VIDEOS, self
        )

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.video_import_button)
        self.layout.addWidget(self.view_video_list_button)
        self.layout.addWidget(self.play_pause_videos_button)

    def import_videos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Open Files", "", "Video Files (*.mp4);;All Files (*)"
        )
        self.state.data["video_list"] = files

        if files:
            for file in files:
                self.main_window.status_component.set_and_log_status(f"Imported {file}")
