from tkinter import ttk, Menu
from component_interface import ComponentInterface
from create_random_segments_modal_frame import CreateRandomSegmentsModalFrame
from export_youtube_timestamp_modal_frame import ExportYoutubeTimestampModalFrame


# videos input
class MenuFrame(ttk.Frame, ComponentInterface):
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

    def show_create_random_segments_modal(self):
        self.modal = CreateRandomSegmentsModalFrame(self.master)

    def show_export_youtube_timestamp_modal(self):
        self.modal = ExportYoutubeTimestampModalFrame(self.master)
