import os
import pytest
from video_utils import VideoUtils
from file_utils import FileUtils


output_directory = os.path.join("src", "test")
test_mp4_name = "2023_04_15_19_00_49.mp4"  # this video has a duration of 15 seconds
test_aac_name = "long_duration_audio.aac"
output_name = "test_concatenate_videos.mp4"
output_combined_name = "test_combined.mp4"
output_trimmed_name = "test_trimmed.mp4"
concatenated_video_path = FileUtils.get_file_path(
    os.path.join(output_directory, output_name)
)
combined_video_path = FileUtils.get_file_path(
    os.path.join(output_directory, output_combined_name)
)
trimmed_video_path = FileUtils.get_file_path(
    os.path.join(output_directory, output_trimmed_name)
)
test_video_path = FileUtils.get_file_path(os.path.join(output_directory, test_mp4_name))
test_audio_path = FileUtils.get_file_path(os.path.join(output_directory, test_aac_name))


@pytest.fixture(autouse=True)
def before_each():
    clean_up_test_files()

    assert os.path.exists(concatenated_video_path) == False

    yield

    clean_up_test_files()


def clean_up_test_files():
    # clean up
    if os.path.exists(concatenated_video_path):
        os.remove(concatenated_video_path)
    if os.path.exists(combined_video_path):
        os.remove(combined_video_path)
    if os.path.exists(trimmed_video_path):
        os.remove(trimmed_video_path)


def test_get_video_duration():
    assert VideoUtils.get_video_duration(test_video_path) == 15


def test_get_ffmpeg_preset_value_for_nvenc_h264():
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("faster") == "fast"
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("veryslow") == "slow"
    assert VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("medium") == "medium"
    assert (
        VideoUtils.get_ffmpeg_preset_value_for_nvenc_h264("not-a-valid-preset")
        == "medium"
    )


def test_concatenate_videos():
    videos = [test_video_path, test_video_path]  # each video duration = 15s
    VideoUtils.concatenate_videos(videos, output_directory, output_name)
    assert os.path.exists(concatenated_video_path) == True
    assert VideoUtils.get_video_duration(concatenated_video_path) == 30


def test_combine_mp4_aac_to_mp4():
    VideoUtils.combine_mp4_aac_to_mp4(
        test_video_path, test_audio_path, output_directory, output_combined_name
    )
    assert os.path.exists(combined_video_path) == True
    assert VideoUtils.get_video_duration(combined_video_path) == 15


def test_trim_mp4_by_timestamp():
    VideoUtils.trim_mp4_by_timestamp(
        test_video_path,
        "0:00:05",
        "0:00:10",
        1920,
        1080,
        "ultrafast",
        trimmed_video_path,
    )
    assert os.path.exists(trimmed_video_path) == True
    assert VideoUtils.get_video_duration(trimmed_video_path) == 5


def test_get_video_resolution():
    width, height = VideoUtils.get_video_resolution(test_video_path)
    assert width == 1920
    assert height == 1080
