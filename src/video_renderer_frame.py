import os
from tkinter import ttk
import tkinter as tk
from tkVideoPlayer import TkinterVideo


# video renderer
class VideoRendererFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

    def refresh(self):
        # dynamically create video player instances
        self.videoplayers = []
        for i in range(len(self.master.video_list)):
            videoplayer = TkinterVideo(self, scaled=True, keep_aspect=True)
            videoplayer.load(os.path.abspath(self.master.video_list[i]))
            videoplayer.grid(row=0, column=i, sticky="NEWS",
                             padx=(10), pady=(20))
            self.videoplayers.append(videoplayer)

    def play_all(self):
        self.master.master.status_component.set_and_log_status(
            "playing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.play()

    def pause_all(self):
        self.master.master.status_component.set_and_log_status(
            "pausing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.pause()
