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
        videoplayer_1 = TkinterVideo(self, scaled=True)
        videoplayer_1.load(r"/Users/shihanxiong/Downloads/Tv_1280x720.mp4")
        videoplayer_1.grid(row=0, column=0, sticky="W")
        videoplayer_1.play()
        # videoplayer_1.pause()

        # video player #2
        videoplayer_2 = TkinterVideo(self, scaled=True)
        videoplayer_2.load(
            r"/Users/shihanxiong/Downloads/SampleVideo_1280x720_20mb.mp4")
        videoplayer_2.grid(row=0, column=1, sticky="E")
        videoplayer_2.play()
        # videoplayer_2.pause()
