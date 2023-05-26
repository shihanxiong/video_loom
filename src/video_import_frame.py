import tkinter as tk
from tkinter import ttk, Toplevel, filedialog as fd


class VideoImportFrame(ttk.Frame):
    _TITLE_VIEW_VIDEO_LIST = "View Videos List"

    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.video_import_button = ttk.Button(
            self, text="Import videos", padding=(10), command=self.select_file
        )
        self.view_video_list_button = ttk.Button(
            self,
            text="View video list",
            padding=(10),
            command=self.show_videos_list_modal,
        )
        self.play_pause_videos_button = ttk.Button(
            self,
            text="Play all videos",
            state="disable",
            padding=(10),
            command=self.play_pause,
        )

        self.video_import_button.grid(row=1, column=0, sticky="EW")
        self.view_video_list_button.grid(row=1, column=1, sticky="EW")
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
        self.close_modal()

    def play_pause(self):
        if self.play_pause_videos_button["state"] == "enable":
            if self.is_playing == True:
                self.master.video_renderer_component.pause_all()
                self.play_pause_videos_button.config(text="Play all videos")
                self.is_playing = False
            else:
                self.master.video_renderer_component.play_all()
                self.play_pause_videos_button.config(text="Pause all videos")
                self.is_playing = True

    def show_videos_list_modal(self):
        self.modal = Toplevel(self.master.master)
        self.modal.title(self._TITLE_VIEW_VIDEO_LIST)

        # layout
        self.modal.columnconfigure(0, weight=0)
        self.modal.columnconfigure(1, weight=0)
        self.modal.columnconfigure(2, weight=0)

        for idx, video in enumerate(self.master.video_list):
            self.modal.rowconfigure(idx, weight=0)
            file_idx = ttk.Label(self.modal, text=f"video {idx + 1} -->", padding=(20))
            file_idx.grid(row=idx, column=0, sticky="EW")

            file_name = ttk.Label(self.modal, text=video, padding=(20))
            file_name.grid(row=idx, column=1, sticky="EW")

            delete_button = ttk.Button(
                self.modal,
                text="Remove",
                padding=(10),
                command=lambda: self.remove_file_from_list(idx),
            )
            delete_button.grid(row=idx, column=2, sticky="EW", padx=(10))

        clear_videos_list_button = ttk.Button(
            self.modal,
            text="Clear video list",
            padding=(10),
            command=self.clear_video_list,
        )
        close_modal_button = ttk.Button(
            self.modal,
            text="Close",
            padding=(10),
            command=self.close_modal,
        )

        clear_videos_list_button.grid(
            row=len(self.master.video_list),
            column=0,
            columnspan=2,
            sticky="EW",
            padx=(10),
            pady=(10),
        )
        close_modal_button.grid(
            row=len(self.master.video_list), column=2, sticky="EW", padx=(10), pady=(10)
        )

    def remove_file_from_list(self, idx):
        del self.master.video_list[idx]
        self.close_modal()

    def close_modal(self):
        self.master.master.app_refresh()
        self.modal.destroy()
