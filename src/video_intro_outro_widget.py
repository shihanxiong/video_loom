from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog
from global_state import GlobalState


class VideoIntroOutroWidget(QWidget):
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
        self.import_intro_button = QPushButton(self._BUTTON_TEXT_IMPORT_INTRO, self)
        self.import_intro_button.clicked.connect(
            lambda: self.import_intro_or_outro(self._INTRO)
        )
        self.import_outro_button = QPushButton(self._BUTTON_TEXT_IMPORT_OUTRO, self)
        self.import_outro_button.clicked.connect(
            lambda: self.import_intro_or_outro(self._OUTRO)
        )

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.import_intro_button)
        self.layout.addWidget(self.import_outro_button)

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
