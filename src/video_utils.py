import os
import subprocess
import logging
import json
from file_utils import FileUtils
from sys_utils import SysUtils


class VideoUtils:
    def __init__(self):
        pass

    @staticmethod
    # returns [Integer] the duration of the video in seconds
    def get_video_duration(video):
        ffprobe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            video,
        ]
        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        try:
            duration = json.loads(output)["format"]["duration"]
            return int(float(duration))
        except (json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def get_ffmpeg_preset_value_for_nvenc_h264(ffmpeg_preset_value):
        """
        this method is used to translate FFMPEG presets into nvenc encoder presets

        when using CPU encoding, ffmpeg allows presets to be:
        'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'
        when using GPU encoding, ffmpeg nvenc_h264 allows presets to be:
        'slow', 'medium', 'fast'
        """
        if (
            ffmpeg_preset_value == "ultrafast"
            or ffmpeg_preset_value == "superfast"
            or ffmpeg_preset_value == "veryfast"
            or ffmpeg_preset_value == "faster"
            or ffmpeg_preset_value == "fast"
        ):
            return "fast"
        elif (
            ffmpeg_preset_value == "slow"
            or ffmpeg_preset_value == "slower"
            or ffmpeg_preset_value == "veryslow"
        ):
            return "slow"
        else:
            return "medium"

    @staticmethod
    def concatenate_videos(
        videos, output_directory, output_name, ffmpeg_preset_value="ultrafast"
    ):
        try:
            output_file = os.path.join(output_directory, output_name)
            cmd = ["ffmpeg"]

            for video in videos:
                cmd.extend(["-i", video])

            cmd.extend(
                [
                    "-filter_complex",
                    "concat=n={}:v=1:a=1".format(len(videos)),
                    "-c:v",
                    "libx264",
                    "-c:a",
                    "aac",
                    "-preset",
                    ffmpeg_preset_value,
                    output_file,
                ]
            )

            subprocess.run(cmd, text=True, check=True)
            return output_file
        except Exception as err:
            logging.error(f"{VideoUtils.__name__}: {str(err)}")

    @staticmethod
    # returns [String] the path of the output file
    def combine_mp4_aac_to_mp4(
        source_video,
        source_audio,
        output_directory,
        output_file,
        ffmpeg_preset_value="ultrafast",
    ):
        try:
            output_file_path = os.path.join(output_directory, output_file)
            cmd = [
                "ffmpeg",
                "-i",
                source_video,
                "-i",
                source_audio,
                "-c:v",
                "copy",
                "-map",
                "0:v",
                "-map",
                "1:a",
                "-shortest",
                "-preset",
                ffmpeg_preset_value,
                output_file_path,
            ]

            subprocess.run(cmd, text=True, check=True)
            return output_file_path
        except Exception as err:
            logging.error(f"{VideoUtils.__name__}: {str(err)}")
