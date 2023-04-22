import tkinter as tk
import logging
from tkinter import ttk, Menu, Toplevel, Entry, END
from timeline_utils import TimelineUtils
from sys_utils import SysUtils


# videos input
class MenuFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # file
        file_menu = Menu(menubar, font=self.master.default_font, tearoff="off")
        # file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            font=self.master.default_font,
            command=self.master.destroy,
        )

        # segment
        segment_menu = Menu(
            menubar, font=self.master.default_font, tearoff="off")
        segment_menu.add_command(
            label="create random segments",
            font=self.master.default_font,
            command=self.show_create_random_segments_modal,
        )

        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        menubar.add_cascade(label="Segment", menu=segment_menu, underline=0)

    def refresh(self):
        pass

    def disable_menu_item(self, label):
        pass

    def enable_menu_item(self, label):
        pass

    def show_create_random_segments_modal(self):
        self.modal = Toplevel(self.master)
        self.modal.title("create random segments")

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
        number_of_videos_label.grid(row=0, column=0, sticky="W")
        self.number_of_videos_input = Entry(
            self.modal, font=self.master.default_font)
        self.number_of_videos_input.grid(row=0, column=1)

        number_of_segments_label = ttk.Label(
            self.modal, text="Number of segments", padding=(20)
        )
        number_of_segments_label.grid(row=1, column=0, sticky="W")
        self.number_of_segments_input = Entry(
            self.modal, font=self.master.default_font)
        self.number_of_segments_input.grid(row=1, column=1)

        minutes_per_segment_label = ttk.Label(
            self.modal, text="Minutes per segment", padding=(20)
        )
        minutes_per_segment_label.grid(row=2, column=0, sticky="W")
        self.minutes_per_segment_input = Entry(
            self.modal, font=self.master.default_font)
        self.minutes_per_segment_input.grid(row=2, column=1)

        confirm_button = ttk.Button(
            self.modal,
            text="Confirm",
            padding=(10),
            command=self.generate_segments,
        )
        confirm_button.grid(row=3, column=0, sticky="E")
        cancel_button = ttk.Button(
            self.modal, text="Cancel", padding=(10), command=self.close_modal
        )
        cancel_button.grid(row=3, column=1, sticky="W")

    def generate_segments(self):
        try:
            random_segments_text = TimelineUtils.generate_random_segments(
                num_segments=int(self.number_of_segments_input.get()),
                min_per_segment=int(self.minutes_per_segment_input.get()),
                num_videos=int(self.number_of_videos_input.get()),
            )
            self.master.timeline_component.timeline_text.insert(
                END, random_segments_text)
            self.master.status_component.set_and_log_status(
                "random segments generated")
            self.close_modal()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def close_modal(self):
        self.modal.destroy()
