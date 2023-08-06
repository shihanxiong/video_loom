from tkinter import ttk
from component_interface import ComponentInterface
from video_list_modal_frame import VideoListModalFrame
from tktooltip import ToolTip


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
        ToolTip(
            self.video_import_button,
            msg="Select video files to import",
            delay=0,
        )
        self.view_video_list_button = ttk.Button(
            self,
            text="View video list (0 of 4)",
            command=self.show_videos_list_modal,
        )
        ToolTip(
            self.view_video_list_button,
            msg="Display / manage videos currently imported",
            delay=0,
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
        self.modal = VideoListModalFrame(self.master)
