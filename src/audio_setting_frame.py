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

        audio_setting_label = ttk.Label(
            self, text="Audio Settings", padding=(10))
        audio_setting_label.grid(row=0, columnspan=2)

        audio_track_label = ttk.Label(self, text="audio track:")
        audio_track_label.grid(row=1, column=0, sticky="E")
        self.audio_track_selection = ttk.Combobox(
            self, width=14, textvariable=self.audio_track_variable, state="readonly", font=self.master.master.default_font)
        self.audio_track_selection.grid(row=1, column=1)
        self.audio_track_selection['values'] = (1, 2, 3, 4)
        self.audio_track_selection.current(0)  # default - 1

    def refresh(self):
        self.audio_track_selection['values'] = tuple(
            range(1, len(self.master.master.video_component.video_list) + 1))

    def get_audio_track(self):
        return self.audio_track_variable.get()
