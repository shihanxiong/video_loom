import tkinter as tk
from tkinter import ttk, filedialog as fd


class VideoImportFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.video_import_button = ttk.Button(
            self, text="Import a video", padding=(10), command=self.select_file)
        self.video_import_button.grid(row=1, column=0, sticky="EW")
        self.clear_video_list_button = ttk.Button(
            self, text="Clear video list", padding=(10), command=self.clear_video_list)
        self.clear_video_list_button.grid(row=1, column=1, sticky="EW")
        self.play_all_videos_button = ttk.Button(self, text="Play all videos", state="disable", padding=(
            10), command=self.master.video_renderer_component.play_all)
        self.play_all_videos_button.grid(row=1, column=2, sticky="EW")
        self.pause_all_videos_button = ttk.Button(self, text="Pause all videos", state="disable", padding=(
            10), command=self.master.video_renderer_component.pause_all)
        self.pause_all_videos_button.grid(row=1, column=3, sticky="EW")

    def refresh(self):
        if len(self.master.video_list) > 0:
            self.set_buttons_status(
                [self.play_all_videos_button, self.pause_all_videos_button], "enable")
        else:
            self.set_buttons_status(
                [self.play_all_videos_button, self.pause_all_videos_button], "disable")

        if len(self.master.video_list) == self.master.max_num_of_videos:
            self.set_buttons_status([self.video_import_button], "disable")
        else:
            self.set_buttons_status([self.video_import_button], "enable")

    def select_file(self):
        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.*')
        )

        filenames = fd.askopenfilenames(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filenames != None:
            self.master.video_list += filenames
            self.master.master.app_refresh()
            self.master.master.status_component.set_and_log_status(
                f"Imported {filenames}")

    def clear_video_list(self):
        self.master.video_list = []
        self.master.master.app_refresh()
        self.master.master.status_component.set_and_log_status(
            "video list cleared")

    def set_buttons_status(self, buttons, status):
        for button in buttons:
            button["state"] = status
