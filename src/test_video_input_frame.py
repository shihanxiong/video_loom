import tkinter as tk
from freezegun import freeze_time
from video_frame import VideoFrame


@freeze_time("1990-02-08 01:23:45")
def test_get_current_timestamp():
    video_frame = VideoFrame(tk.Tk())
    assert video_frame.get_current_timestamp() == '1990_02_08_01_23_45'
