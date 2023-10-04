from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from audio_setting_widget import AudioSettingWidget
from video_setting_widget import VideoSettingWidget


class SettingsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # components
        self.main_window = main_window
        self.audio_setting_component = AudioSettingWidget(main_window)
        self.video_setting_component = VideoSettingWidget()

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.audio_setting_component)
        self.layout.addWidget(self.video_setting_component)
