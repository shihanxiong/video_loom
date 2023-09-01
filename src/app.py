import os
from sys import platform
import tkinter as tk
import logging
from async_tkinter_loop import async_mainloop
from tkinter import ttk
from windows import set_dpi_awareness
from menu_frame import MenuFrame
from video_frame import VideoFrame
from settings_frame import SettingsFrame
from timeline_frame import TimelineFrame
from toolbar_frame import ToolbarFrame
from status_frame import StatusFrame
from time_utils import TimeUtils
from file_utils import FileUtils
from sys_utils import SysUtils


class VideoLoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_configure()

        # app config
        self.title(f"Video Loom - {FileUtils.get_latest_version_from_changelog()}")
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.default_font = ("Courier", 14)
        style = ttk.Style(self)
        style.configure(".", font=self.default_font)
        self.option_add("*TCombobox*Listbox.font", self.default_font)

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

        # app layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

        # components
        component_padding = (10, 10)
        self.menu_component = MenuFrame(self)
        self.video_component = VideoFrame(self, padding=component_padding)
        self.settings_component = SettingsFrame(self, padding=component_padding)
        self.timeline_component = TimelineFrame(self, padding=component_padding)
        self.status_component = StatusFrame(self, padding=component_padding)
        self.toolbar_component = ToolbarFrame(self, padding=component_padding)

        self.video_component.grid(row=0, sticky="NEW")
        self.settings_component.grid(row=1, sticky="NEW")
        self.timeline_component.grid(row=2, sticky="NEW")
        self.status_component.grid(row=3, sticky="NEW")
        self.toolbar_component.grid(row=4, sticky="NEW")

        # register all components
        self.components = [
            self.menu_component,
            self.video_component,
            self.settings_component,
            self.timeline_component,
            self.status_component,
            self.toolbar_component,
        ]

    # Setup high resolution in windows 10 (high DPI does not apply to MacOS)
    # Setup window height respectively, default to 1000x1000 for Linux
    def app_configure(self):
        if SysUtils.is_win32():
            set_dpi_awareness()
            # self.resizable(False, False) # TODO: render display in scale for non-4k monitors
            self.window_height = 1100
            self.window_width = 1200
        elif SysUtils.is_macos():
            self.window_height = 900
            self.window_width = 1000
        else:
            self.window_height = 1000
            self.window_width = 1000

    def app_refresh(self):
        for component in self.components:
            component.refresh()


try:
    if __name__ == "__main__":
        # start app
        root = VideoLoom()

        # set app logo in UI
        if SysUtils.is_running_in_pyinstaller_bundle():
            root.iconbitmap(
                FileUtils.get_bundled_file_path(os.path.join("app_logo.ico"))
            )
        else:
            root.iconbitmap(
                FileUtils.get_file_path(os.path.join("img", "app_logo.ico"))
            )

        async_mainloop(root)
except Exception as err:
    logging.error(f"app.py: {str(err)}")
