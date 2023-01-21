from sys import platform
import tkinter as tk
from tkinter import ttk
from windows import set_dpi_awareness
from video_frame import VideoFrame
from audio_setting_frame import AudioSettingFrame
from timeline_frame import TimelineFrame
from toolbar_frame import ToolbarFrame
from status_frame import StatusFrame


class VideoLoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_configure()
        self.title("Video Loom - v0.81-beta")
        self.geometry(f"{self.window_width}x{self.window_height}")

        # app config
        self.default_font = ("Courier", 14)
        style = ttk.Style(self)
        style.configure('.', font=self.default_font)

        # app layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

        # components
        self.video_component = VideoFrame(self, padding=(10, 10))
        self.video_component.grid(row=0, sticky="NEW")
        self.audio_setting_component = AudioSettingFrame(self, padding=(10, 0))
        self.audio_setting_component.grid(row=1, sticky="NEW")
        self.timeline_component = TimelineFrame(self, padding=(10, 10))
        self.timeline_component.grid(row=2, sticky="SEW")
        self.status_component = StatusFrame(self, padding=(10, 10))
        self.status_component.grid(row=3, sticky="NEW")
        self.toolbar_component = ToolbarFrame(self, padding=(10, 10))
        self.toolbar_component.grid(row=4, sticky="NEW")

    # Setup high resolution in windows 10 (high DPI does not apply to MacOS)
    # Setup window height respectively
    def app_configure(self):
        if platform == "win32":
            set_dpi_awareness()
            self.resizable(False, False)
            self.window_height = 1100
            self.window_width = 1100
        elif platform == "darwin":
            self.window_height = 900
            self.window_width = 1000
        else:
            pass


# start app
root = VideoLoom()
root.mainloop()
