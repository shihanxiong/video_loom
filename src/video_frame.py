import os
import subprocess
import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from video_import_frame import VideoImportFrame
from video_renderer_frame import VideoRendererFrame
from video_control_frame import VideoControlFrame
from video_intro_outro_frame import VideoIntroOutroFrame
from time_utils import TimeUtils
from file_utils import FileUtils
from timeline_utils import TimelineUtils
from audio_utils import AudioUtils
from sys_utils import SysUtils
from video_utils import VideoUtils
from component_interface import ComponentInterface


# videos input
class VideoFrame(ttk.Frame, ComponentInterface):
    _PROCESS_VIDEO_ERROR_MESSAGE = "An error occurred while generating video :("

    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.max_num_of_videos = 4
        self.intro = None
        self.outro = None
        self.video_list = []
        self.trimmed_video_list = []
        self.output_directory = os.getcwd()
        self.output_file_name = tk.StringVar(
            value=f"{TimeUtils.get_current_timestamp()}.mp4"
        )
        self.output_width = 0
        self.output_height = 0

        # layout - rows
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1, minsize=220)
        self.rowconfigure(3, weight=1)

        # layout - columns
        self.total_columns = 4
        for c_idx in range(self.total_columns):
            self.columnconfigure(c_idx, weight=1)

        # video rendering
        self.video_renderer_component = VideoRendererFrame(self, padding=(10, 0))
        self.video_renderer_component.grid(row=2, columnspan=4, sticky="NEWS")

        # video import / clear
        self.video_import_component = VideoImportFrame(self, padding=(10, 0))
        self.video_import_component.grid(row=0, columnspan=4, sticky="NEW")

        # video intro / outro
        self.video_intro_outro_component = VideoIntroOutroFrame(self, padding=(10, 0))
        self.video_intro_outro_component.grid(row=1, columnspan=4, sticky="NEW")

        # video control
        self.video_control_component = VideoControlFrame(self, padding=(10, 0))
        self.video_control_component.grid(row=3, columnspan=4, sticky="NEW")

        # register all components
        self.components = [
            self.video_import_component,
            self.video_intro_outro_component,
            self.video_renderer_component,
            self.video_control_component,
        ]

    def refresh(self):
        for component in self.components:
            component.refresh()

    def generate_video_with_ffmpeg(self):
        # remove output file if exists
        FileUtils.clean_up_temp_files()

        # calculate output video resolution
        # this will scale all inputs to match the max width & max height
        self.calculate_output_resolutions()

        # calculate output video max durations
        self.calculate_video_durations()

        # logging
        start_time = datetime.now()
        logging.info("kicking off video processing, hang tight")
        logging.info(
            f"using audio track {self.master.settings_component.audio_setting_component.get_audio_track()}"
        )
        logging.info("================timeline start================")
        logging.info(self.master.timeline_component.get_timeline_text())
        logging.info("================timeline end==================")

        # video processing
        try:
            # validate timeline
            error = TimelineUtils.validate_timeline(
                self.master.timeline_component.get_timeline_text(), self.video_durations
            )

            if error is None:
                self.master.status_component.set_and_log_status("timeline validated")
            else:
                self.master.status_component.set_and_log_status(error)
                return

            # determine processing speed
            self.ffmpeg_preset_value = (
                self.master.settings_component.video_setting_component.get_ffmpeg_preset_value()
            )

            self.master.status_component.set_and_log_status(
                f"Setting processing speed to be {self.master.settings_component.video_setting_component.get_ffmpeg_preset_value()}"
            )

            # trim videos
            self.process_trimmed_videos()

            # concanete only when at least 2 video segments
            if len(self.trimmed_video_list) > 1:
                # concatenate trimmed videos
                output_file = self.concatenate_trimmed_videos()

                # get audio from selected video
                output_sound = self.process_audio()

                # combine video and audio into final file
                final_file = self.finalize_video(output_file, output_sound)

                # add intro and outro if exists
                self.add_intro_outro(final_file)
        except Exception as err:
            self.master.status_component.set_and_log_status(
                "An error occurred while generating video :("
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

        # logging
        end_time = datetime.now()
        self.master.status_component.set_and_log_status(
            f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds"
        )
        self.master.app_refresh()

    def calculate_output_resolutions(self):
        self.output_width = 0
        self.output_height = 0

        # Get information about the videos
        for video in self.video_list:
            width, height = VideoUtils.get_video_resolution(video)
            self.output_width = max(self.output_width, width)
            self.output_height = max(self.output_height, height)

        self.master.status_component.set_and_log_status(
            f"output resolution is determined at {self.output_width} x {self.output_height}"
        )

    def calculate_video_durations(self):
        self.video_durations = {}

        # Get video durations
        for idx, video in enumerate(self.video_list):
            duration = VideoUtils.get_video_duration(video)
            self.video_durations[idx + 1] = duration

        self.master.status_component.set_and_log_status(
            f"output durations info processed"
        )

    def process_trimmed_videos(self):
        try:
            parsed_timeline_arr = TimelineUtils.parse_timeline(
                self.master.timeline_component.get_timeline_text()
            )

            for idx, timeline in enumerate(parsed_timeline_arr):
                video, start, end = timeline
                trimmed_output = os.path.join(
                    self.output_directory, f"trimmed_{idx}.mp4"
                )
                self.trimmed_video_list.append(trimmed_output)

                VideoUtils.trim_mp4_by_timestamp(
                    self.video_list[int(video) - 1],
                    start,
                    end,
                    self.output_width,
                    self.output_height,
                    self.ffmpeg_preset_value,
                    trimmed_output,
                )

            self.master.status_component.set_and_log_status("completed trimming videos")
        except Exception as err:
            self.master.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def concatenate_trimmed_videos(self):
        try:
            output_file = VideoUtils.concatenate_videos(
                self.trimmed_video_list,
                self.output_directory,
                "output.mp4",
                self.ffmpeg_preset_value,
            )
            self.master.status_component.set_and_log_status(
                "completed concatenating trimmed videos"
            )

            return output_file
        except Exception as err:
            self.master.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def process_audio(self):
        try:
            output_sound = os.path.join(self.output_directory, "audio.aac")
            input_video = self.video_list[
                self.master.settings_component.audio_setting_component.get_audio_track()
                - 1
            ]
            AudioUtils.generate_aac_from_mp4(
                input_video, output_sound, self.ffmpeg_preset_value
            )
            self.master.status_component.set_and_log_status(
                f"completed processing {output_sound} from video {input_video}"
            )

            return output_sound
        except Exception as err:
            self.master.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def finalize_video(self, output_file, output_sound):
        try:
            final_file = VideoUtils.combine_mp4_aac_to_mp4(
                output_file,
                output_sound,
                self.output_directory,
                self.output_file_name.get(),
            )
            self.master.status_component.set_and_log_status(
                "video is processed and ready for use"
            )
            return final_file
        except Exception as err:
            self.master.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def add_intro_outro(self, final_file):
        try:
            videos = []

            if self.intro != None:
                videos.append(self.intro)

            videos.append(final_file)

            if self.outro != None:
                videos.append(self.outro)

            # if intro or outro is detected, we concatenate them into the final video
            if len(videos) > 1:
                VideoUtils.concatenate_videos(
                    videos,
                    self.output_directory,
                    f"{TimeUtils.get_current_timestamp()}_with_intro_outro.mp4",
                    self.ffmpeg_preset_value,
                )
        except Exception as err:
            self.master.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")
