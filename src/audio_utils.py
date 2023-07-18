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
            # using preset=ultrafast as the audio is for preview only
            cmd = [
                "ffmpeg",
                "-i",
                mp4_input_filename,
                "-vn",
                "-acodec",
                "mp3",
                "-preset",
                ffmpeg_preset_value,
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
                "-preset",
                ffmpeg_preset_value,
                aac_output_filename,
            ]
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

            # Prepare the ffmpeg command
            cmd = ["ffmpeg"]

            # Add input options for each file
            for audio in audios:
                cmd.extend(["-i", audio])

            # Add the concatenate filter
            filter_string = "concat:" + "|".join(f"[{i}:0]" for i in range(len(audios)))
            cmd.extend(["-filter_complex", filter_string, "-c:a", "copy"])

            # Set the output file
            cmd.append(output_file)

            # Run the ffmpeg command
            subprocess.run(
                cmd,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if SysUtils.is_win32() else 0,
            )
        except Exception as err:
            logging.error(f"{AudioUtils.__name__}: {str(err)}")
