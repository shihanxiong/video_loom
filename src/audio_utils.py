import subprocess
import logging
from file_utils import FileUtils


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

        subprocess.run(cmd, text=True, check=True)
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
        subprocess.run(cmd, text=True, check=True)

        return aac_output_filename
