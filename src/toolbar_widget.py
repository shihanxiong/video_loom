import os
import logging
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QCoreApplication
from global_state import GlobalState
from file_utils import FileUtils
from timeline_utils import TimelineUtils
from video_utils import VideoUtils
from audio_utils import AudioUtils
from time_utils import TimeUtils


class ToolbarWidget(QWidget):
    _PROCESS_VIDEO_ERROR_MESSAGE = "An error occurred while generating video :("

    def __init__(self, main_window):
        super().__init__()

        # state
        self.state = GlobalState()
        self.output_directory = os.getcwd()
        self.trimmed_video_list = []

        # components
        self.main_window = main_window
        self.generate_button = QPushButton("Generate Video", self)
        self.generate_button.clicked.connect(self.generate_video_with_ffmpeg)
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(QCoreApplication.quit)

        # component layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.quit_button)

    def calculate_output_resolutions(self):
        self.output_width = 0
        self.output_height = 0

        # Get information about the videos
        for video in self.state.data["video_list"]:
            width, height = VideoUtils.get_video_resolution(video)
            self.output_width = max(self.output_width, width)
            self.output_height = max(self.output_height, height)

        self.main_window.status_component.set_and_log_status(
            f"output resolution is determined at {self.output_width} x {self.output_height}"
        )

    def calculate_video_durations(self):
        self.video_durations = {}

        # Get video durations
        for idx, video in enumerate(self.state.data["video_list"]):
            duration = VideoUtils.get_video_duration(video)
            self.video_durations[idx + 1] = duration

        self.main_window.status_component.set_and_log_status(
            f"output durations info processed"
        )

    def process_trimmed_videos(self):
        try:
            parsed_timeline_arr = TimelineUtils.parse_timeline(
                self.state.data["timeline"]
            )

            for idx, timeline in enumerate(parsed_timeline_arr):
                video, start, end = timeline
                trimmed_output = os.path.join(
                    self.output_directory, f"trimmed_{idx}.mp4"
                )
                self.trimmed_video_list.append(trimmed_output)

                VideoUtils.trim_mp4_by_timestamp(
                    self.state.data["video_list"][int(video) - 1],
                    start,
                    end,
                    self.output_width,
                    self.output_height,
                    self.state.data["ffmpeg_preset_value"],
                    trimmed_output,
                )

            self.main_window.status_component.set_and_log_status(
                "completed trimming videos"
            )
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def concatenate_trimmed_videos(self):
        try:
            output_file = VideoUtils.concatenate_videos(
                self.trimmed_video_list,
                self.output_directory,
                "output.mp4",
                self.state.data["ffmpeg_preset_value"],
            )
            self.main_window.status_component.set_and_log_status(
                "completed concatenating trimmed videos"
            )

            return output_file
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def process_audio(self):
        try:
            output_sound = os.path.join(self.output_directory, "audio.aac")
            input_video = self.state.data["video_list"][
                self.state.data["audio_track_selection"] - 1
            ]
            AudioUtils.generate_aac_from_mp4(
                input_video, output_sound, self.state.data["ffmpeg_preset_value"]
            )
            self.main_window.status_component.set_and_log_status(
                f"completed processing {output_sound} from video {input_video}"
            )

            return output_sound
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def finalize_video(self, output_file, output_sound):
        try:
            final_file = VideoUtils.combine_mp4_aac_to_mp4(
                output_file,
                output_sound,
                self.output_directory,
                f"{TimeUtils.get_current_timestamp()}.mp4",
            )
            self.main_window.status_component.set_and_log_status(
                "video is processed and ready for use"
            )
            return final_file
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def add_intro_outro(self, final_file):
        try:
            videos = []

            if self.state.data["intro"] != None:
                videos.append(self.sate.data["intro"])

            videos.append(final_file)

            if self.state.data["outro"] != None:
                videos.append(self.state.data["outro"])

            # if intro or outro is detected, we concatenate them into the final video
            if len(videos) > 1:
                VideoUtils.concatenate_videos(
                    videos,
                    self.output_directory,
                    f"{TimeUtils.get_current_timestamp()}_with_intro_outro.mp4",
                    self.state.data["ffmpeg_preset_value"],
                )
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                self._PROCESS_VIDEO_ERROR_MESSAGE
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def generate_video_with_ffmpeg(self):
        if len(self.state.data["video_list"]) == 0 or self.state.data["timeline"] == "":
            return

        # remove output file if exists
        FileUtils.clean_up_temp_files()

        # calculate output video resolution
        # this will scale all inputs to match the max width & max height
        self.calculate_output_resolutions()

        # calculate output video max durations
        self.calculate_video_durations()

        # logging
        start_time = datetime.now()
        self.main_window.status_component.set_and_log_status(
            "kicking off video processing, hang tight"
        )
        self.main_window.status_component.set_and_log_status(
            f"using audio track {self.state.data['audio_track_selection']}"
        )
        logging.info("================timeline start================")
        logging.info(self.state.data["timeline"])
        logging.info("================timeline end==================")

        # video processing
        try:
            # validate timeline
            error = TimelineUtils.validate_timeline(
                self.state.data["timeline"], self.video_durations
            )

            if error is None:
                self.main_window.status_component.set_and_log_status(
                    "timeline validated"
                )
            else:
                self.main_window.status_component.set_and_log_status(error)
                return

            self.main_window.status_component.set_and_log_status(
                f"Setting processing speed to be {self.state.data['ffmpeg_preset_value']}"
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

            # logging
            end_time = datetime.now()
            self.main_window.status_component.set_and_log_status(
                f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds"
            )
        except Exception as err:
            self.main_window.status_component.set_and_log_status(
                "An error occurred while generating video :( (see log file for more detail)"
            )
            logging.error(f"{self.__class__.__name__}: {str(err)}")
