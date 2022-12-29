import tkinter as tk
from tkinter import ttk
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
