import logging
from tkinter import ttk, Toplevel, Entry, END
from timeline_utils import TimelineUtils


class CreateRandomSegmentsModalFrame(Toplevel):
    _MODAL_TITLE = "create random segments"

    def __init__(self, parent):
        super().__init__(parent)
        self.title(self._MODAL_TITLE)
        self.parent = parent

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        # props
        number_of_videos_label = ttk.Label(self, text="Number of videos", padding=(20))
        self.number_of_videos_input = Entry(self, font=self.master.default_font)
        number_of_segments_label = ttk.Label(
            self, text="Number of segments", padding=(20)
        )
        self.number_of_segments_input = Entry(self, font=self.master.default_font)
        minutes_per_segment_label = ttk.Label(
            self, text="Minutes per segment", padding=(20)
        )
        self.minutes_per_segment_input = Entry(self, font=self.master.default_font)
        confirm_button = ttk.Button(
            self,
            text="Confirm",
            padding=(10),
            command=self.generate_segments,
        )
        cancel_button = ttk.Button(
            self, text="Cancel", padding=(10), command=self.close
        )

        number_of_videos_label.grid(row=0, column=0, sticky="W")
        self.number_of_videos_input.grid(row=0, column=1, padx=(0, 40))

        number_of_segments_label.grid(row=1, column=0, sticky="W")
        self.number_of_segments_input.grid(row=1, column=1, padx=(0, 40))

        minutes_per_segment_label.grid(row=2, column=0, sticky="W")
        self.minutes_per_segment_input.grid(row=2, column=1, padx=(0, 40))

        confirm_button.grid(row=3, column=0, sticky="E", pady=(0, 20))
        cancel_button.grid(row=3, column=1, sticky="W", pady=(0, 20))

    def generate_segments(self):
        try:
            random_segments_text = TimelineUtils.generate_random_segments(
                num_segments=int(self.number_of_segments_input.get()),
                min_per_segment=int(self.minutes_per_segment_input.get()),
                num_videos=int(self.number_of_videos_input.get()),
            )
            self.master.timeline_component.timeline_text.insert(
                END, random_segments_text
            )
            self.master.status_component.set_and_log_status("random segments generated")
            self.close()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def close(self):
        self.destroy()
