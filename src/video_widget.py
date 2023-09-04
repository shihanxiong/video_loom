from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from video_import_widget import VideoImportWidget
from video_renderer_widget import VideoRendererWidget
from video_control_widget import VideoControlWidget


class VideoWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # components
        self.video_import_component = VideoImportWidget(main_window)
        self.video_renderer_component = VideoRendererWidget()
        self.video_control_component = VideoControlWidget()

        # app layout
        grid = QVBoxLayout()
        grid.addWidget(self.video_import_component)
        grid.addWidget(self.video_renderer_component)
        grid.addWidget(self.video_control_component)
        self.setLayout(grid)
