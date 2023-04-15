import os
from audio_utils import AudioUtils
from file_utils import FileUtils


def test_generate_mp3_from_mp4():
    mp3_output_filename = "test_generate_mp3_from_mp4.mp3"
    mp3_path = FileUtils.get_file_path(
        os.path.join("src", "test", mp3_output_filename))
    mp4_path = FileUtils.get_file_path(
        os.path.join("src", "test", "2023_04_15_19_00_49.mp4"))

    # clean up
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
    assert (os.path.exists(mp3_path) == False)

    AudioUtils.generate_mp3_from_mp4(mp4_path, mp3_path)
    assert (os.path.exists(mp3_path) == True)
