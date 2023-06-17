import logging
from tkinter import ttk, Toplevel, Entry
from timeline_utils import TimelineUtils


class ExportYoutubeTimestampModalFrame(Toplevel):
    _MODAL_TITLE = "export YouTube timestamp"

    def __init__(self, parent):
        super().__init__(parent)
        self.title(self._MODAL_TITLE)
        self.parent = parent

        # props
        num_of_videos = len(self.master.video_component.video_list)
        self.entries = []

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        for i in range(num_of_videos):
            self.rowconfigure(i, weight=0)
            label = ttk.Label(self, text=f"Label {i + 1}", padding=(20))
            label.grid(row=i, column=0, sticky="EW")

            entry = Entry(self, font=self.master.default_font)
            entry.grid(row=i, column=1, columnspan=2, sticky="EW", padx=(0, 40))
            self.entries.append(entry)

        confirm_button = ttk.Button(
            self,
            text="Copy to clipboard",
            padding=(10),
            command=self.export_youtube_timestamp,
        )
        cancel_button = ttk.Button(
            self, text="Cancel", padding=(10), command=self.close
        )

        confirm_button.grid(row=num_of_videos, column=1, sticky="EW", pady=(0, 20))
        cancel_button.grid(
            row=num_of_videos, column=2, sticky="EW", padx=(0, 40), pady=(0, 20)
        )

    def export_youtube_timestamp(self):
        try:
            timeline_text = self.master.timeline_component.get_timeline_text()

            # get labels
            labels = []
            for entry in self.entries:
                labels.append(entry.get())

            # generate youtube timestamp
            timestamp_text = TimelineUtils.generate_youtube_timestamp(
                timeline_text, labels
            )

            # copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(timestamp_text)
            self.update()

            # close modal
            self.close()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def close(self):
        self.destroy()
