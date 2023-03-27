import tkinter as tk
from tkinter import ttk


# toolbar
class ToolbarFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.generate_button = ttk.Button(self, text="Generate Video", state="disable", padding=(
            10), command=self.master.video_component.generate_video_with_ffmpeg)
        self.generate_button.grid(row=0, column=0, sticky="EW")

        self.quit_button = ttk.Button(
            self, text="Quit", padding=(10), command=self.master.destroy)
        self.quit_button.grid(row=0, column=1, sticky="EW")

    def refresh(self):
        if len(self.master.video_component.video_list) == 0:
            self.disable_generate_button()
        else:
            self.enable_generate_button()

    def disable_generate_button(self):
        self.generate_button["state"] = "disable"

    def enable_generate_button(self):
        self.generate_button["state"] = "enable"
