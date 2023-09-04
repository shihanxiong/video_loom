from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class VideoImportWidget(QWidget):
    _TITLE_VIEW_VIDEO_LIST = "View Videos List"
    _BUTTON_TEXT_PLAY_ALL_VIDEOS = "Play all videos"
    _BUTTON_TEXT_PAUSE_ALL_VIDEOS = "Pause all videos"

    def __init__(self):
        super().__init__()

        # components
        self.video_import_button = QPushButton("Import videos", self)
        self.view_video_list_button = QPushButton("View video list (0 of 4)", self)
        self.play_pause_videos_button = QPushButton(
            self._BUTTON_TEXT_PLAY_ALL_VIDEOS, self
        )

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.video_import_button)
        self.layout.addWidget(self.view_video_list_button)
        self.layout.addWidget(self.play_pause_videos_button)
