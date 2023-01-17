import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
import cv2


# video renderer
class VideoRendererFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.grid(row=2, sticky="NEW")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # video renderer
        # video player #1
        self.videoplayer_1 = TkinterVideo(self, scaled=True)
        self.videoplayer_1.grid(row=0, column=0, sticky="W")

        # video player #2
        self.videoplayer_2 = TkinterVideo(self, scaled=True)
        self.videoplayer_2.grid(row=0, column=1, sticky="E")

    def load_videos(self):
        self.videoplayer_1.load(self.master.video_list[0])
        self.videoplayer_2.load(self.master.video_list[1])

    def play_all(self):
        self.master.master.status_component.set_and_log_status(
            "playing all videos")
        self.videoplayer_1.play()
        self.videoplayer_2.play()

    def pause_all(self):
        self.master.master.status_component.set_and_log_status(
            "pausing all videos")
        self.videoplayer_1.pause()
        self.videoplayer_2.pause()
