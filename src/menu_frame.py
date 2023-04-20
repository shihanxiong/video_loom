import tkinter as tk
from tkinter import ttk, Menu, Toplevel


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
            label='Exit',
            command=self.master.destroy,
        )

        # segment
        segment_menu = Menu(
            menubar, font=self.master.default_font, tearoff="off")
        segment_menu.add_command(
            label='create random segments',
            command=self.show_create_random_segments_modal
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu,
            underline=0
        )
        menubar.add_cascade(
            label="Segment",
            menu=segment_menu,
            underline=0
        )

    def refresh(self):
        pass

    def disable_menu_item(self, label):
        pass

    def enable_menu_item(self, label):
        pass

    def show_create_random_segments_modal(self):
        modal = Toplevel(self.master)
        modal.title("create random segments")
        modal.geometry("450x220")

        # layout
        modal.rowconfigure(0, weight=0)
        modal.rowconfigure(1, weight=0)
        modal.rowconfigure(2, weight=0)
        modal.columnconfigure(0, weight=0)
        modal.columnconfigure(1, weight=0)

        # props
        number_of_segments_label = ttk.Label(
            modal, text="Number of segments", padding=(20))
        number_of_segments_label.grid(row=0, column=0)
        minutes_per_segment_label = ttk.Label(
            modal, text="Minutes per segment", padding=(20))
        minutes_per_segment_label.grid(row=1, column=0)
