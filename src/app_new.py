import os
import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QPixmap
from file_utils import FileUtils
from time_utils import TimeUtils
from sys_utils import SysUtils
from video_widget import VideoWidget
from settings_widget import SettingsWidget
from timeline_widget import TimelineWidget
from status_widget import StatusWidget
from toolbar_widget import ToolbarWidget


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # app config
        self.setGeometry(400, 400, 1000, 400)
        self.setWindowTitle(
            f"Video Loom - {FileUtils.get_latest_version_from_changelog()}"
        )
        icon_path = FileUtils.get_file_path(
            os.path.join("src", "assets", "img", "app_logo.png")
        )
        if SysUtils.is_running_in_pyinstaller_bundle():
            icon_path = FileUtils.get_bundled_file_path(os.path.join("app_logo.png"))

        self.setWindowIcon(QIcon(QPixmap(icon_path)))

        # self.setStyleSheet("background-color:green")
        # self.setWindowOpacity(0.5)

        # initialize logging
        log_formatter = logging.Formatter(
            fmt="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # file handler
        file_handler = logging.FileHandler(f"{TimeUtils.get_current_date()}.log")
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

        # components
        self.central_widget = QWidget()
        self.video_component = VideoWidget(self)
        self.settings_component = SettingsWidget()
        self.timeline_component = TimelineWidget()
        self.status_component = StatusWidget(self)
        self.toolbar_component = ToolbarWidget()

        # app layout
        grid = QVBoxLayout()
        grid.addWidget(self.video_component)
        grid.addWidget(self.settings_component)
        grid.addWidget(self.timeline_component)
        grid.addWidget(self.status_component)
        grid.addWidget(self.toolbar_component)
        self.central_widget.setLayout(grid)
        self.setCentralWidget(self.central_widget)


try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = App()
        window.show()
        sys.exit(app.exec())
except Exception as err:
    logging.error(f"app.py: {str(err)}")
