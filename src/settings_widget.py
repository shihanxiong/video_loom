from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from audio_setting_widget import AudioSettingWidget
from video_setting_widget import VideoSettingWidget


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # components
        self.audio_setting_component = AudioSettingWidget()
        self.video_setting_component = VideoSettingWidget()

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.audio_setting_component)
        self.layout.addWidget(self.video_setting_component)
