import tkinter as tk
from tkinter import ttk


class VideoSelectFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # select buttons
        self.select_video_button_1 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.master.timeline_component.insert_timestamp(0))
        self.select_video_button_1.grid(row=0, column=0, sticky="EW")
        self.select_video_button_2 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.master.timeline_component.insert_timestamp(1))
        self.select_video_button_2.grid(row=0, column=1, sticky="EW")
        self.select_video_button_3 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.master.timeline_component.insert_timestamp(2))
        self.select_video_button_3.grid(row=0, column=2, sticky="EW")
        self.select_video_button_4 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.master.timeline_component.insert_timestamp(3))
        self.select_video_button_4.grid(row=0, column=3, sticky="EW")

    def refresh(self):
        pass
