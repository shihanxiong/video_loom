import os
import ffmpeg

video_1 = ffmpeg.input(
    "/Users/shihanxiong/Downloads/Tv_1280x720.mp4")
video_2 = ffmpeg.input(
    "/Users/shihanxiong/Downloads/SampleVideo_1280x720_20mb.mp4")
video_3 = ffmpeg.input(
    "/Users/shihanxiong/Downloads/nasdaq_bell_ringing.mp4")
output_file_name = "output.mp4"

if os.path.exists(output_file_name):
    os.remove(output_file_name)

# video_1.output('1.mp4', **{'qscale:v': 1}).run()
# video_2.output('2.mp4', **{'qscale:v': 1}).run()
# video_3.output('3.mp4', **{'qscale:v': 1}).run()

video_1 = ffmpeg.input("/Users/shihanxiong/dev/video_loom/1.mp4")
video_2 = ffmpeg.input("/Users/shihanxiong/dev/video_loom/2.mp4")
video_3 = ffmpeg.input("/Users/shihanxiong/dev/video_loom/3.mp4")

ffmpeg.concat(
    video_1.trim(start=1, end=5),
    video_2.trim(start=5, end=10),
    video_3.trim(start=10, end=15),
).output(output_file_name, vsync="2", **{'c:v': 'libx264', 'c:a': 'copy', 'b:v': '6000k', 'qscale:v': 3}).run()
