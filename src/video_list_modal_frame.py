from tkinter import ttk, Toplevel


class VideoListModalFrame(Toplevel):
    _MODAL_TITLE = "view video list"

    def __init__(self, parent):
        super().__init__(parent)
        self.title(self._MODAL_TITLE)
        self.parent = parent

        row_count = 0

        # layout
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        for idx, video in enumerate(self.master.video_list):
            self.rowconfigure(idx, weight=0)
            file_idx = ttk.Label(self, text=f"video {idx + 1} -->", padding=(20))
            file_idx.grid(row=idx, column=0, sticky="EW")

            file_name = ttk.Label(self, text=video, padding=(20))
            file_name.grid(row=idx, column=1, sticky="EW")

            delete_button = ttk.Button(
                self,
                text="Remove",
                padding=(10),
                # below see https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
                command=lambda i=idx: self.remove_file_from_list(i),
            )
            delete_button.grid(row=idx, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count = idx + 1

        if self.master.intro != None:
            self.rowconfigure(row_count, weight=0)
            file_idx = ttk.Label(self, text=f"intro -->", padding=(20))
            file_idx.grid(row=row_count, column=0, sticky="EW")

            file_name = ttk.Label(self, text=self.master.intro, padding=(20))
            file_name.grid(row=row_count, column=1, sticky="EW")

            delete_button = ttk.Button(
                self,
                text="Remove",
                padding=(10),
                command=lambda: self.remove_intro(),
            )
            delete_button.grid(row=row_count, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count += 1

        if self.master.outro != None:
            self.rowconfigure(row_count, weight=0)
            file_idx = ttk.Label(self, text=f"outro -->", padding=(20))
            file_idx.grid(row=row_count, column=0, sticky="EW")

            file_name = ttk.Label(self, text=self.master.outro, padding=(20))
            file_name.grid(row=row_count, column=1, sticky="EW")

            delete_button = ttk.Button(
                self,
                text="Remove",
                padding=(10),
                command=lambda: self.remove_outro(),
            )
            delete_button.grid(row=row_count, column=2, sticky="EW", padx=(10))

            # update row_count
            row_count += 1

        clear_videos_list_button = ttk.Button(
            self,
            text="Clear video list",
            padding=(10),
            command=self.clear_video_list,
        )
        close_modal_button = ttk.Button(
            self,
            text="Close",
            padding=(10),
            command=self.close,
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

    def clear_video_list(self):
        self.master.video_list = []
        self.master.intro = None
        self.master.outro = None
        self.master.master.app_refresh()
        self.master.master.status_component.set_and_log_status("video list cleared")
        self.close()

    def remove_file_from_list(self, idx):
        del self.master.video_list[idx]
        self.close()

    def remove_intro(self):
        self.master.intro = None
        self.close()

    def remove_outro(self):
        self.master.outro = None
        self.close()

    def close(self):
        self.master.master.app_refresh()
        self.destroy()
