import tkinter as tk
from tkinter import ttk


# audio setting
class AudioSettingFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.audio_track_variable = tk.IntVar()

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        audio_setting_label = ttk.Label(
            self, text="Audio Settings", padding=(10))
        audio_setting_label.grid(row=0, columnspan=4)

        audio_track_option_1 = ttk.Radiobutton(
            self, text="Audio track 1", variable=self.audio_track_variable, value=0)
        audio_track_option_2 = ttk.Radiobutton(
            self, text="Audio track 2", variable=self.audio_track_variable, value=1)
        audio_track_option_3 = ttk.Radiobutton(
            self, text="Audio track 3", variable=self.audio_track_variable, value=2)
        audio_track_option_4 = ttk.Radiobutton(
            self, text="Audio track 4", variable=self.audio_track_variable, value=3)
        audio_track_option_1.grid(row=1, column=0)
        audio_track_option_2.grid(row=1, column=1)
        audio_track_option_3.grid(row=1, column=2)
        audio_track_option_4.grid(row=1, column=3)

    def refresh(self):
        pass
