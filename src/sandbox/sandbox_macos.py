import os
import glob
import subprocess


input_video_a = "/Users/shihanxiong/Downloads/Tv_1280x720.mp4"
input_video_b = "/Users/shihanxiong/Downloads/SampleVideo_1280x720_20mb.mp4"
output_directory = "./src/sandbox/output"

# remove temp files
try:
    for f in glob.glob(f"{output_directory}/*.mp4"):
        os.remove(f)
    for f in glob.glob(f"{output_directory}/*.aac"):
        os.remove(f)
except OSError:
    pass

# Define the start and end times of the segment to extract
start_time = "00:00:01"
end_time = "00:00:05"

# Get information about the videos
cmd = f"ffprobe -v error -show_entries stream=width,height -of csv=p=0 {input_video_a}"
output = subprocess.check_output(cmd, shell=True)
width_a, height_a = output.decode().strip().split(",")
video_a_larger = int(width_a) > int(height_a)

cmd = f"ffprobe -v error -show_entries stream=width,height -of csv=p=0 {input_video_b}"
output = subprocess.check_output(cmd, shell=True)
width_b, height_b = output.decode().strip().split(",")
video_b_larger = int(width_b) > int(height_b)

# Determine which video has the larger resolution
if video_a_larger and int(width_a) > int(width_b):
    larger_width, larger_height = int(width_a), int(height_a)
else:
    larger_width, larger_height = int(width_b), int(height_b)

# Trim video A
output_a = f"{output_directory}/video_a_trimmed.mp4"
cmd = f"ffmpeg -i {input_video_a} -ss {start_time} -to {end_time} -vf scale={larger_width}:{larger_height} -c:a copy {output_a}"
subprocess.check_output(cmd, shell=True)

# Trim video B
output_b = f"{output_directory}/video_b_trimmed.mp4"
cmd = f"ffmpeg -i {input_video_b} -ss {start_time} -to {end_time} -vf scale={larger_width}:{larger_height} -c:a copy {output_b}"
subprocess.check_output(cmd, shell=True)

# Concatenate the two trimmed videos
output_file = f"{output_directory}/output.mp4"
cmd = f"ffmpeg -i {output_a} -i {output_b} -filter_complex '[0:v][1:v]concat=n=2:v=1:a=0' -c:v libx264 -crf 23 -preset medium -y -vsync 2 {output_file}"
subprocess.check_output(cmd, shell=True)

# Get the sound from video B for the given time frame
output_sound = f"{output_directory}/audio_b_trimmed.aac"
# cmd = f"ffmpeg -i {input_video_b} -ss {start_time} -to {end_time} -vn -acodec copy {output_sound}" # TODO: calculate end_time based on the total time
cmd = f"ffmpeg -i {input_video_b} -ss {start_time} -to 00:00:09 -vn -acodec copy {output_sound}"
subprocess.check_output(cmd, shell=True)

# Add the sound from video B to the final output file
final_file = f"{output_directory}/final.mp4"
cmd = f"ffmpeg -i {output_file} -i {output_sound} -map 0:v -map 1:a -c copy -shortest -y -vsync 2 {final_file}"
subprocess.check_output(cmd, shell=True)
