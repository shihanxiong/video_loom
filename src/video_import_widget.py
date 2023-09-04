from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QGridLayout
from PyQt6.QtCore import Qt
from global_state import GlobalState


class VideoImportWidget(QWidget):
    _TITLE_VIEW_VIDEO_LIST = "View Videos List"
    _BUTTON_TEXT_PLAY_ALL_VIDEOS = "Play all videos"
    _BUTTON_TEXT_PAUSE_ALL_VIDEOS = "Pause all videos"
    _BUTTON_TEXT_IMPORT_INTRO = "Add intro"
    _BUTTON_TEXT_IMPORT_OUTRO = "Add outro"
    _INTRO = "Intro"
    _OUTRO = "Outro"

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
        self.view_video_list_button.setEnabled(False)  # TODO
        self.play_pause_videos_button = QPushButton(
            self._BUTTON_TEXT_PLAY_ALL_VIDEOS, self
        )
        self.play_pause_videos_button.setEnabled(False)  # TODO
        self.import_intro_button = QPushButton(self._BUTTON_TEXT_IMPORT_INTRO, self)
        self.import_intro_button.clicked.connect(
            lambda: self.import_intro_or_outro(self._INTRO)
        )
        self.import_outro_button = QPushButton(self._BUTTON_TEXT_IMPORT_OUTRO, self)
        self.import_outro_button.clicked.connect(
            lambda: self.import_intro_or_outro(self._OUTRO)
        )

        # component layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.video_import_button, 0, 0)
        self.layout.addWidget(self.view_video_list_button, 0, 1)
        self.layout.addWidget(self.play_pause_videos_button, 0, 2)
        self.layout.addWidget(self.import_intro_button, 1, 0)
        self.layout.addWidget(self.import_outro_button, 1, 2)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)

    def import_videos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Open Files", "", "Video Files (*.mp4);;All Files (*)"
        )
        self.state.data["video_list"] = files

        if files:
            for file in files:
                self.main_window.status_component.set_and_log_status(f"Imported {file}")

    def import_intro_or_outro(self, type):
        file, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Video Files (*.mp4);;All Files (*)"
        )

        if type == self._INTRO:
            self.state.data["intro"] = file
        elif type == self._OUTRO:
            self.state.data["outro"] = file

        self.main_window.status_component.set_and_log_status(
            f"Imported {file} as {type}"
        )
