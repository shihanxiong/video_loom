import os
import pytest
from audio_utils import AudioUtils
from file_utils import FileUtils
from pdb import set_trace  # call set_trace() inline to setup debugger


mp3_output_filename = "test_generate_mp3_from_mp4.mp3"
aac_output_filename = "test_generate_aac_from_mp4.aac"
mp3_path = FileUtils.get_file_path(
    os.path.join("src", "test", mp3_output_filename))
aac_path = FileUtils.get_file_path(
    os.path.join("src", "test", aac_output_filename))
mp4_path = FileUtils.get_file_path(
    os.path.join("src", "test", "2023_04_15_19_00_49.mp4"))
ffmpeg_preset_arg = "-preset ultrafast"


def clean_up_test_files():
    # clean up
    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    if os.path.exists(aac_path):
        os.remove(aac_path)


@pytest.fixture(autouse=True)
def before_each():
    clean_up_test_files()

    assert (os.path.exists(mp3_path) == False)
    assert (os.path.exists(aac_path) == False)

    yield

    clean_up_test_files()


def test_generate_mp3_from_mp4():
    AudioUtils.generate_mp3_from_mp4(mp4_path, mp3_path)
    assert (os.path.exists(mp3_path) == True)


def test_generate_aac_from_mp4():
    AudioUtils.generate_aac_from_mp4(mp4_path, aac_path, ffmpeg_preset_arg)
    assert (os.path.exists(aac_path) == True)
