import tkinter as tk
from tkinter import ttk


# video setting
class VideoSettingFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.ffmpeg_preset_arg = tk.StringVar()

        video_setting_label = ttk.Label(
            self, text="Video Settings", padding=(10))
        video_setting_label.grid(row=0, columnspan=2)

        ffmpeg_preset_label = ttk.Label(self, text="process speed:")
        ffmpeg_preset_label.grid(row=1, column=0, sticky="E")
        ffmpeg_preset_selection = ttk.Combobox(
            self, width=14, textvariable=self.ffmpeg_preset_arg, state="readonly", font=self.master.master.default_font)
        ffmpeg_preset_selection.grid(row=1, column=1)
        ffmpeg_preset_selection['values'] = (
            'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow')
        ffmpeg_preset_selection.current(5)  # default - 'medium'

    def refresh(self):
        pass

    def get_ffmpeg_preset_value(self):
        return self.ffmpeg_preset_arg.get()
