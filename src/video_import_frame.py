import tkinter as tk
from tkinter import ttk, Toplevel, filedialog as fd
from component_interface import ComponentInterface


class VideoImportFrame(ttk.Frame, ComponentInterface):
    _TITLE_VIEW_VIDEO_LIST = "View Videos List"
    _BUTTON_TEXT_PLAY_ALL_VIDEOS = "Play all videos"
    _BUTTON_TEXT_PAUSE_ALL_VIDEOS = "Pause all videos"

    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.video_import_button = ttk.Button(
            self, text="Import videos", command=self.import_videos
        )
        self.view_video_list_button = ttk.Button(
            self,
            text="View video list (0 of 4)",
            command=self.show_videos_list_modal,
        )
        self.play_pause_videos_button = ttk.Button(
            self,
            text=self._BUTTON_TEXT_PLAY_ALL_VIDEOS,
            state="disable",
            command=self.play_pause,
        )

        self.video_import_button.grid(row=1, column=0, sticky="EW")
        self.view_video_list_button.grid(row=1, column=1, sticky="EW")
        self.play_pause_videos_button.grid(row=1, column=2, sticky="EW")

        self.is_playing = False

    def refresh(self):
        if len(self.master.video_list) > 0:
            self.enable_button(self.play_pause_videos_button)
        else:
            self.disable_button(self.play_pause_videos_button)

        if len(self.master.video_list) == self.master.max_num_of_videos:
            self.disable_button(self.video_import_button)
        else:
            self.enable_button(self.video_import_button)

        self.set_button_text(
            self.view_video_list_button,
            f"View video list ({len(self.master.video_list)} of {self.master.max_num_of_videos})",
        )

    def import_videos(self):
        filenames = self.select_files()

        if filenames != None:
            self.master.video_list += filenames
            self.master.master.app_refresh()
            self.master.master.status_component.set_and_log_status(
                f"Imported {filenames}"
            )

    def clear_video_list(self):
        self.master.video_list = []
        self.master.intro = None
        self.master.outro = None
        self.master.master.app_refresh()
        self.master.master.status_component.set_and_log_status("video list cleared")
        self.close_modal()

    def play_pause(self):
        if self.play_pause_videos_button["state"] == "enable":
            if self.is_playing == True:
                self.master.video_renderer_component.pause_all()
                self.set_button_text(
                    self.play_pause_videos_button, self._BUTTON_TEXT_PLAY_ALL_VIDEOS
                )
                self.is_playing = False
            else:
                self.master.video_renderer_component.play_all()
                self.set_button_text(
                    self.play_pause_videos_button, self._BUTTON_TEXT_PAUSE_ALL_VIDEOS
                )
                self.is_playing = True

    def show_videos_list_modal(self):
        self.modal = Toplevel(self.master.master)
        self.modal.title(self._TITLE_VIEW_VIDEO_LIST)
        row_count = 0

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
                # below see https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
                command=lambda i=idx: self.remove_file_from_list(i),
            )
            delete_button.grid(row=idx, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count = idx + 1

        if self.master.intro != None:
            self.modal.rowconfigure(row_count, weight=0)
            file_idx = ttk.Label(self.modal, text=f"intro -->", padding=(20))
            file_idx.grid(row=row_count, column=0, sticky="EW")

            file_name = ttk.Label(self.modal, text=self.master.intro, padding=(20))
            file_name.grid(row=row_count, column=1, sticky="EW")

            delete_button = ttk.Button(
                self.modal,
                text="Remove",
                padding=(10),
                command=lambda: self.remove_intro(),
            )
            delete_button.grid(row=row_count, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count += 1

        if self.master.outro != None:
            self.modal.rowconfigure(row_count, weight=0)
            file_idx = ttk.Label(self.modal, text=f"outro -->", padding=(20))
            file_idx.grid(row=row_count, column=0, sticky="EW")

            file_name = ttk.Label(self.modal, text=self.master.outro, padding=(20))
            file_name.grid(row=row_count, column=1, sticky="EW")

            delete_button = ttk.Button(
                self.modal,
                text="Remove",
                padding=(10),
                command=lambda: self.remove_outro(),
            )
            delete_button.grid(row=row_count, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count += 1

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
            row=row_count,
            column=0,
            columnspan=2,
            sticky="EW",
            padx=(10),
            pady=(10),
        )
        close_modal_button.grid(
            row=row_count, column=2, sticky="EW", padx=(10), pady=(10)
        )

    def remove_file_from_list(self, idx):
        del self.master.video_list[idx]
        self.close_modal()

    def remove_intro(self):
        self.master.intro = None
        self.close_modal()

    def remove_outro(self):
        self.master.outro = None
        self.close_modal()

    def close_modal(self):
        self.master.master.app_refresh()
        self.modal.destroy()
