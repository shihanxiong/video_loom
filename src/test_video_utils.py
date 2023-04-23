from video_utils import VideoUtils


def test_get_ffmpeg_preset_value_for_nvenc_h264():
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("faster") == "fast"
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("veryslow") == "slow"
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("medium") == "medium"
    assert (
        VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("not-a-valie-preset")
        == "medium"
    )
