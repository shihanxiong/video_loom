import os
import subprocess
import logging
import json
from sys_utils import SysUtils


class AudioUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_mp3_from_mp4(
        mp4_input_filename, mp3_output_filename, ffmpeg_preset_value="ultrafast"
    ):
        try:
            # Note: -preset is for video encoding, not audio. For MP3 encoding,
            # we use -q:a for quality instead. Using -q:a 2 for high quality.
            cmd = [
                "ffmpeg",
                "-i",
                mp4_input_filename,
                "-vn",
                "-acodec",
                "mp3",
                "-q:a",
                "2",
                mp3_output_filename,
            ]

            subprocess.run(
                cmd,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if SysUtils.is_win32() else 0,
            )
            # TODO: do logging via status_component instead
            logging.debug(
                f"generated {mp3_output_filename} from video {mp4_input_filename}"
            )

            return mp3_output_filename
        except Exception as err:
            logging.error(f"{AudioUtils.__name__}: {str(err)}")

    @staticmethod
    def generate_aac_from_mp4(
        mp4_input_filename, aac_output_filename, ffmpeg_preset_value
    ):
        try:
            cmd = [
                "ffmpeg",
                "-i",
                mp4_input_filename,
                "-vn",
                "-acodec",
                "copy",
                "-shortest",
                aac_output_filename,
            ]
            # Note: -preset is for video encoding, not audio. When using -acodec copy,
            # we're copying the stream without re-encoding, so -preset doesn't apply.
            subprocess.run(
                cmd,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if SysUtils.is_win32() else 0,
            )

            return aac_output_filename
        except Exception as err:
            logging.error(f"{AudioUtils.__name__}: {str(err)}")

    @staticmethod
    def get_audio_duration(audio):
        # TODO: combine this function w/ VideoUtils.get_video_duration()
        ffprobe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            audio,
        ]
        result = subprocess.run(
            ffprobe_cmd,
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if SysUtils.is_win32() else 0,
        )
        output = result.stdout

        try:
            duration = json.loads(output)["format"]["duration"]
            return int(float(duration))
        except (json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def concatenate_audios(audios, output_directory, output_name):
        try:
            output_file = os.path.join(output_directory, output_name)

            # Use concat demuxer for simple concatenation
            # Format: concat:file1|file2|file3
            concat_string = "concat:"
            for idx, audio in enumerate(audios):
                if idx != 0:
                    concat_string += "|"
                concat_string += audio

            cmd = [
                "ffmpeg",
                "-i",
                concat_string,
                "-c",
                "copy",
                output_file,
            ]

            # Run the ffmpeg command
            subprocess.run(
                cmd,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if SysUtils.is_win32() else 0,
            )
        except Exception as err:
            logging.error(f"{AudioUtils.__name__}: {str(err)}")
