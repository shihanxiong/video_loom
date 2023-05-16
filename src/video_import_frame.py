import tkinter as tk
from tkinter import ttk, filedialog as fd


class VideoImportFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.video_import_button = ttk.Button(
            self, text="Import videos", padding=(10), command=self.select_file
        )
        self.video_import_button.grid(row=1, column=0, sticky="EW")
        self.clear_video_list_button = ttk.Button(
            self, text="Clear video list", padding=(10), command=self.clear_video_list
        )
        self.clear_video_list_button.grid(row=1, column=1, sticky="EW")
        self.play_pause_videos_button = ttk.Button(
            self,
            text="Play all videos",
            state="disable",
            padding=(10),
            command=self.play_pause,
        )
        self.play_pause_videos_button.grid(row=1, column=2, sticky="EW")
        self.is_playing = False

    def refresh(self):
        if len(self.master.video_list) > 0:
            self.play_pause_videos_button["state"] = "enable"
        else:
            self.play_pause_videos_button["state"] = "disable"

        if len(self.master.video_list) == self.master.max_num_of_videos:
            self.video_import_button["state"] = "disable"
        else:
            self.video_import_button["state"] = "enable"

    def select_file(self):
        filetypes = (("video files", "*.mp4"), ("All files", "*.*"))

        filenames = fd.askopenfilenames(
            title="Open a file", initialdir="/", filetypes=filetypes
        )

        if filenames != None:
            self.master.video_list += filenames
            self.master.master.app_refresh()
            self.master.master.status_component.set_and_log_status(
                f"Imported {filenames}"
            )

    def clear_video_list(self):
        self.master.video_list = []
        self.master.master.app_refresh()
        self.master.master.status_component.set_and_log_status("video list cleared")

    def play_pause(self):
        if self.is_playing == True:
            self.master.video_renderer_component.pause_all()
            self.play_pause_videos_button.config(text="Play all videos")
            self.is_playing = False
        else:
            self.master.video_renderer_component.play_all()
            self.play_pause_videos_button.config(text="Pause all videos")
            self.is_playing = True
