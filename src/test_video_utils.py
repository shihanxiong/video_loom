import os
import pytest
from video_utils import VideoUtils
from file_utils import FileUtils


output_directory = os.path.join("src", "test")
test_mp4_name = "2023_04_15_19_00_49.mp4"
output_name = "test_concatenate_videos.mp4"
concatenated_video_path = FileUtils.get_file_path(
    os.path.join(output_directory, output_name)
)
test_video_path = FileUtils.get_file_path(os.path.join(output_directory, test_mp4_name))


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
    videos = [test_video_path, test_video_path]
    assert VideoUtils.concatenate_videos(videos, output_directory, output_name)
    assert os.path.exists(os.path.join(output_directory, output_name)) == True
