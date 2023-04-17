import os
import tkinter as tk
from tkinter import ttk
from audio_utils import AudioUtils
from file_utils import FileUtils


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

        audio_track_label = ttk.Label(self, text="audio track:")
        audio_track_label.grid(row=1, column=0, sticky="E")
        self.audio_track_selection = ttk.Combobox(
            self, width=14, textvariable=self.audio_track_variable, state="readonly", font=self.master.master.default_font)
        self.audio_track_selection.grid(row=1, column=1)
        self.audio_track_selection['values'] = (1, 2, 3, 4)
        self.audio_track_selection.current(0)  # default - 1
        self.generate_audio_preview_button = ttk.Button(
            self, text="Generate preview", command=self.generate_audio_preview)
        self.generate_audio_preview_button.grid(row=1, column=2)
        self.remove_audio_preview_button = ttk.Button(
            self, text="Remove preview", command=self.remove_audio_preview)
        self.remove_audio_preview_button.grid(row=1, column=3, sticky="W")
        self.remove_audio_preview_button["state"] = "disable"
        self.audio_track_selection.bind(
            "<<ComboboxSelected>>", self.component_refresh)

    def refresh(self):
        self.audio_track_selection['values'] = tuple(
            range(1, len(self.master.master.video_component.video_list) + 1))
        self.component_refresh()

    def component_refresh(self, _=None):
        if self.has_audio_preview():
            self.generate_audio_preview_button["state"] = "disable"
            self.remove_audio_preview_button["state"] = "enable"
        else:
            self.generate_audio_preview_button["state"] = "enable"
            self.remove_audio_preview_button["state"] = "disable"

        # refresh audio currently playing
        self.master.master.video_component.video_renderer_component.load_audio_preview()

    def get_audio_track(self):
        return self.audio_track_variable.get()

    def get_audio_preview_filename(self):
        return f"audio_preview_{self.get_audio_track()}.mp3"

    def get_audio_preview(self):
        return FileUtils.get_file_path(self.get_audio_preview_filename())

    def has_audio_preview(self):
        return os.path.exists(self.get_audio_preview())

    def remove_audio_preview(self):
        # pause all videos
        self.master.master.video_component.video_import_component.pause_all()

        if self.has_audio_preview():
            self.master.master.video_component.video_renderer_component.unload_audio_preview()
            os.remove(FileUtils.get_file_path(
                self.get_audio_preview_filename()))
        self.component_refresh()
        self.master.master.status_component.set_and_log_status(
            f"Audio preview deleted for audio track {self.get_audio_track()}")

    def generate_audio_preview(self):
        self.master.master.status_component.set_and_log_status(
            "Generating audio preview, please wait ...")

        # if videos are playing, pausing them during the process
        self.master.master.video_component.video_renderer_component.pause_all()

        video_list = self.master.master.video_component.video_list
        # no videos imported
        if len(video_list) == 0:
            return

        video_input = self.master.master.video_component.video_list[self.get_audio_track(
        ) - 1]
        audio_preview_output = self.get_audio_preview_filename()
        AudioUtils.generate_mp3_from_mp4(
            FileUtils.escape_file_name(video_input), audio_preview_output)

        # refresh app state
        self.master.master.app_refresh()
        self.master.master.status_component.set_and_log_status(
            f"Audio preview generated for audio track {self.get_audio_track()}")
