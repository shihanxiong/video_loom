import tkinter as tk
from tkinter import ttk
from component_interface import ComponentInterface


# toolbar
class ToolbarFrame(ttk.Frame, ComponentInterface):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.generate_button = ttk.Button(
            self,
            text="Generate Video",
            state="disable",
            padding=(10),
            command=self.master.video_component.generate_video_with_ffmpeg,
        )
        self.quit_button = ttk.Button(
            self, text="Quit", padding=(10), command=self.master.destroy
        )

        self.generate_button.grid(row=0, column=0, sticky="EW")
        self.quit_button.grid(row=0, column=1, sticky="EW")

    def refresh(self):
        if len(self.master.video_component.video_list) == 0:
            self.disable_button(self.generate_button)
        else:
            self.enable_button(self.enable_generate_button)
