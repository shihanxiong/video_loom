import subprocess
import logging


class AudioUtils():
    def __init__(self):
        pass

    @staticmethod
    def generate_mp3_from_mp4(mp4_input_filename, mp3_output_filename):
        # using preset = ultrafast as the audio is for preview only
        cmd = f"ffmpeg -i {mp4_input_filename} -vn -preset ultrafast -acodec mp3 {mp3_output_filename}"
        subprocess.check_output(cmd, shell=True)
        # TODO: do logging via status_component instead
        logging.debug(
            f"generated {mp3_output_filename} from video {mp4_input_filename}")

        return mp3_output_filename

    @staticmethod
    def generate_aac_from_mp4(mp4_input_filename, aac_output_filename, ffmpeg_preset_arg):
        cmd = f"ffmpeg -i {mp4_input_filename} -vn -acodec copy {ffmpeg_preset_arg} {aac_output_filename}"
        subprocess.check_output(cmd, shell=True)

        return aac_output_filename
