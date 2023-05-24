import tkinter as tk
import logging
from tkinter import ttk, Menu, Toplevel, Entry, END
from timeline_utils import TimelineUtils
from sys_utils import SysUtils


# videos input
class MenuFrame(ttk.Frame):
    _MENU_CREATE_RANDOM_SEGMENTS = "create random segments"
    _MENU_EXPORT_YOUTUBE_TIMESTAMP = "export YouTube timestamp"

    def __init__(self, container, **args):
        super().__init__(container, **args)

        # menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # file
        self.file_menu = Menu(menubar, font=self.master.default_font, tearoff="off")
        # file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit",
            font=self.master.default_font,
            command=self.master.destroy,
        )

        # segment
        self.segment_menu = Menu(menubar, font=self.master.default_font, tearoff="off")
        self.segment_menu.add_command(
            label=self._MENU_CREATE_RANDOM_SEGMENTS,
            font=self.master.default_font,
            command=self.show_create_random_segments_modal,
        )
        self.segment_menu.add_command(
            label=self._MENU_EXPORT_YOUTUBE_TIMESTAMP,
            font=self.master.default_font,
            command=self.show_export_youtube_timestamp_modal,
            state="disabled",
        )

        menubar.add_cascade(label="File", menu=self.file_menu, underline=0)
        menubar.add_cascade(label="Segment", menu=self.segment_menu, underline=0)

    def refresh(self):
        if len(self.master.video_component.video_list) == 0:
            self.segment_menu.entryconfig(
                self._MENU_EXPORT_YOUTUBE_TIMESTAMP, state="disabled"
            )
        else:
            self.segment_menu.entryconfig(
                self._MENU_EXPORT_YOUTUBE_TIMESTAMP, state="active"
            )

    def disable_menu_item(self, label):
        pass

    def enable_menu_item(self, label):
        pass

    def show_create_random_segments_modal(self):
        self.modal = Toplevel(self.master)
        self.modal.title(self._MENU_CREATE_RANDOM_SEGMENTS)

        if SysUtils.is_macos():
            self.modal.geometry("380x180")
        elif SysUtils.is_win32():
            self.modal.geometry("520x260")

        # layout
        self.modal.rowconfigure(0, weight=0)
        self.modal.rowconfigure(1, weight=0)
        self.modal.rowconfigure(2, weight=0)
        self.modal.rowconfigure(3, weight=0)
        self.modal.columnconfigure(0, weight=0)
        self.modal.columnconfigure(1, weight=0)

        # props
        number_of_videos_label = ttk.Label(
            self.modal, text="Number of videos", padding=(20)
        )
        self.number_of_videos_input = Entry(self.modal, font=self.master.default_font)
        number_of_segments_label = ttk.Label(
            self.modal, text="Number of segments", padding=(20)
        )
        self.number_of_segments_input = Entry(self.modal, font=self.master.default_font)
        minutes_per_segment_label = ttk.Label(
            self.modal, text="Minutes per segment", padding=(20)
        )
        self.minutes_per_segment_input = Entry(
            self.modal, font=self.master.default_font
        )
        confirm_button = ttk.Button(
            self.modal,
            text="Confirm",
            padding=(10),
            command=self.generate_segments,
        )
        cancel_button = ttk.Button(
            self.modal, text="Cancel", padding=(10), command=self.close_modal
        )

        number_of_videos_label.grid(row=0, column=0, sticky="W")
        self.number_of_videos_input.grid(row=0, column=1)

        number_of_segments_label.grid(row=1, column=0, sticky="W")
        self.number_of_segments_input.grid(row=1, column=1)

        minutes_per_segment_label.grid(row=2, column=0, sticky="W")
        self.minutes_per_segment_input.grid(row=2, column=1)

        confirm_button.grid(row=3, column=0, sticky="E")
        cancel_button.grid(row=3, column=1, sticky="W")

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
            self.close_modal()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def show_export_youtube_timestamp_modal(self):
        self.modal = Toplevel(self.master)
        self.modal.title(self._MENU_EXPORT_YOUTUBE_TIMESTAMP)

        if SysUtils.is_macos():
            self.modal.geometry("380x180")

        # props
        num_of_videos = len(self.master.video_component.video_list)
        self.entries = []

        self.modal.columnconfigure(0, weight=0)
        self.modal.columnconfigure(1, weight=0)
        self.modal.columnconfigure(2, weight=0)
        for i in range(num_of_videos):
            self.modal.rowconfigure(i, weight=0)
            label = ttk.Label(self.modal, text=f"Label {i + 1}", padding=(20))
            label.grid(row=i, column=0, sticky="EW")

            entry = Entry(self.modal, font=self.master.default_font)
            entry.grid(row=i, column=1, columnspan=2, sticky="EW", padx=(0, 40))
            self.entries.append(entry)

        confirm_button = ttk.Button(
            self.modal,
            text="Copy to clipboard",
            padding=(10),
            command=self.export_youtube_timestamp,
        )
        cancel_button = ttk.Button(
            self.modal, text="Cancel", padding=(10), command=self.close_modal
        )

        confirm_button.grid(row=num_of_videos, column=1, sticky="EW", pady=(0, 20))
        cancel_button.grid(
            row=num_of_videos, column=2, sticky="EW", padx=(0, 40), pady=(0, 20)
        )

    def export_youtube_timestamp(self):
        timeline_text = self.master.timeline_component.get_timeline_text()

        # get labels
        labels = []
        for entry in self.entries:
            labels.append(entry.get())

        # generate youtube timestamp
        timestamp_text = TimelineUtils.generate_youtube_timestamp(timeline_text, labels)

        # copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(timestamp_text)
        self.update()

        # close modal
        self.close_modal()

    def close_modal(self):
        self.modal.destroy()
