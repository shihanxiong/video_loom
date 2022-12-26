from sys import platform
import tkinter as tk
from tkinter import ttk
from windows import set_dpi_awareness
from video_input_frame import VideoInputFrame
from audio_setting_frame import AudioSettingFrame
from timeline_frame import TimelineFrame
from toolbar_frame import ToolbarFrame
from status_frame import StatusFrame


class VideoLoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_configure()
        self.title("Video Loom - v1.0-beta")
        self.window_width = 800
        self.window_height = 1000
        self.geometry(f"{self.window_width}x{self.window_height}")

        # app config
        self.default_font = ("Courier", 14)
        style = ttk.Style(self)
        style.configure('.', font=self.default_font)

        # app layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # components
        self.video_component = VideoInputFrame(self, padding=(10, 0))
        self.audio_setting_component = AudioSettingFrame(self, padding=(10, 0))
        self.timeline_component = TimelineFrame(self, padding=(10, 10))
        self.status_component = StatusFrame(self, padding=(10, 10))
        self.toolbar_component = ToolbarFrame(self, padding=(10, 0))

        # events binding
        for i in range(1, 3):
            self.bind(str(i), self.timeline_component.insert_timestamp)

    def app_configure(self):
        if platform == "win32":
            set_dpi_awareness()  # set high resolution in windows 10
            self.resizable(False, False)  # this does not work on MacOS
        elif platform == "darwin":
            pass
        else:
            pass


# start app
root = VideoLoom()
root.mainloop()
