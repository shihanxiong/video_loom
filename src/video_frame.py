import os
import subprocess
import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from video_import_frame import VideoImportFrame
from video_renderer_frame import VideoRendererFrame
from video_control_frame import VideoControlFrame
from time_utils import TimeUtils
from file_utils import FileUtils
from timeline_utils import TimelineUtils
from audio_utils import AudioUtils
from sys_utils import SysUtils


# videos input
class VideoFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.max_num_of_videos = 4
        self.video_list = []
        self.trimmed_video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 4"
        )
        self.output_directory = os.getcwd()
        self.output_file_name = tk.StringVar(
            value=f"{TimeUtils.get_current_timestamp()}.mp4"
        )
        self.output_width = 0
        self.output_height = 0
        self.is_filename_escaped = False

        # layout - rows
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1, minsize=220)
        self.rowconfigure(3, weight=1)

        # layout - columns
        self.total_columns = 4
        for c_idx in range(self.total_columns):
            self.columnconfigure(c_idx, weight=1)

        # video label
        video_label = ttk.Label(self, textvariable=self.video_label_text, padding=(10))
        video_label.grid(row=0, columnspan=4, sticky="N")

        # video rendering
        self.video_renderer_component = VideoRendererFrame(self, padding=(10, 0))
        self.video_renderer_component.grid(row=2, columnspan=4, sticky="NEWS")

        # video import / clear
        self.video_import_component = VideoImportFrame(self, padding=(10, 0))
        self.video_import_component.grid(row=1, columnspan=4, sticky="NEW")

        # video selection
        self.video_control_component = VideoControlFrame(self, padding=(10, 0))
        self.video_control_component.grid(row=3, columnspan=4, sticky="SEW")

        # register all components
        self.components = [
            self.video_import_component,
            self.video_renderer_component,
            self.video_control_component,
        ]

    def refresh(self):
        self.video_label_text.set(
            f"Videos {len(self.video_list)} of {self.max_num_of_videos}"
        )
        logging.debug(f"imported videos {self.video_list}")

        for component in self.components:
            component.refresh()

    def generate_video_with_ffmpeg(self):
        # remove output file if exists
        FileUtils.clean_up_temp_files()

        # for win32|macOS, wrap the video path w/ quotes
        if self.is_filename_escaped == False:
            for idx, video in enumerate(self.video_list):
                self.video_list[idx] = FileUtils.escape_file_name(video)
            self.is_filename_escaped = True

        # calculate output video resolution
        # this will scale all inputs to match the max width & max height
        self.calculate_output_resolutions()

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
            timeline_utils = TimelineUtils()
            error = timeline_utils.validate_timeline(
                self.master.timeline_component.get_timeline_text()
            )

            if error is None:
                self.master.status_component.set_and_log_status("timeline validated")
            else:
                self.master.status_component.set_and_log_status(error)
                return

            # determine processing speed
            self.ffmpeg_preset_arg = f"-preset {self.master.settings_component.video_setting_component.get_ffmpeg_preset_value()}"
            self.master.status_component.set_and_log_status(
                f"Setting processing speed to be {self.master.settings_component.video_setting_component.get_ffmpeg_preset_value()}"
            )

            # trim videos
            self.process_trimmed_videos()

            # concatenate trimmed videos
            output_file = self.concatenate_trimmed_videos()

            # get audio from selected video
            output_sound = self.process_audio()

            # combine video and audio into final file
            self.finalize_video(output_file, output_sound)
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
            cmd = f"ffprobe -v error -show_entries stream=width,height -of csv=p=0 {video}"
            output = subprocess.check_output(cmd, shell=True)
            width, height = output.decode().strip().split(",")
            self.output_width = max(self.output_width, int(width))
            self.output_height = max(self.output_height, int(height))

        self.master.status_component.set_and_log_status(
            f"output resolution is determined at {self.output_width} x {self.output_height}"
        )

    def process_trimmed_videos(self):
        timeline_utils = TimelineUtils()
        parsed_timeline_arr = timeline_utils.parse_timeline(
            self.master.timeline_component.get_timeline_text()
        )

        for idx, timeline in enumerate(parsed_timeline_arr):
            video, start, end = timeline
            trimmed_output = os.path.join(self.output_directory, f"trimmed_{idx}.mp4")
            self.trimmed_video_list.append(trimmed_output)
            cmd = f"ffmpeg -hwaccel cuvid -c:v h264_cuvid -i {self.video_list[int(video) - 1]} -c:v h264_nvenc -ss {start} -to {end} -vf scale_cuda={self.output_width}:{self.output_height} -c:a copy {self.ffmpeg_preset_arg} {FileUtils.escape_file_name(trimmed_output)}"
            subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status("completed trimming videos")

    def concatenate_trimmed_videos(self):
        output_file = os.path.join(self.output_directory, "output.mp4")
        input_args = ""
        ffmpeg_filter = f"'[0:v][1:v]concat=n={len(self.trimmed_video_list)}:v=1:a=0'"

        for trimmed_video in self.trimmed_video_list:
            input_args += f"-i {FileUtils.escape_file_name(trimmed_video)} "

        if SysUtils.is_win32():
            # remove the single quote ' if it's windows
            ffmpeg_filter = f"[0:v][1:v]concat=n={len(self.trimmed_video_list)}:v=1:a=0"

        cmd = f"ffmpeg {input_args} -filter_complex {ffmpeg_filter} -c:v libx264 -crf 23 -y -vsync 2 {self.ffmpeg_preset_arg} {FileUtils.escape_file_name(output_file)}"
        subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "completed concatenating trimmed videos"
        )

        return output_file

    def process_audio(self):
        output_sound = os.path.join(self.output_directory, "audio.aac")
        input_video = self.video_list[
            self.master.settings_component.audio_setting_component.get_audio_track() - 1
        ]
        AudioUtils.generate_aac_from_mp4(
            input_video, output_sound, self.ffmpeg_preset_arg
        )
        self.master.status_component.set_and_log_status(
            f"completed processing {output_sound} from video {input_video}"
        )

        return output_sound

    def finalize_video(self, output_file, output_sound):
        final_file = os.path.join(self.output_directory, self.output_file_name.get())
        cmd = f"ffmpeg -i {FileUtils.escape_file_name(output_file)} -i {FileUtils.escape_file_name(output_sound)} -map 0:v -map 1:a -c copy -shortest -y -vsync 2 {self.ffmpeg_preset_arg} {FileUtils.escape_file_name(final_file)}"
        subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "video is processed and ready for use"
        )
