import subprocess
import logging
from sys_utils import SysUtils


class AudioUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_mp3_from_mp4(
        mp4_input_filename, mp3_output_filename, ffmpeg_preset_value="ultrafast"
    ):
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

    @staticmethod
    def generate_aac_from_mp4(
        mp4_input_filename, aac_output_filename, ffmpeg_preset_value
    ):
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
