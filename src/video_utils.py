class VideoUtils:
    def __init__(self):
        pass

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
