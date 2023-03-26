import os
import subprocess

print(os.getcwd())

# specify input files and timestamps
input_file_1 = "D:\\Game Streaming\\test_video_1.mp4"
input_file_2 = "D:\\Game Streaming\\test_video_2.mp4"
output_file = "output.mp4"
timestamp_1_start = "00:00:01"
timestamp_1_end = "00:00:05"
timestamp_2_start = "00:00:01"
timestamp_2_end = "00:00:05"

# use subprocess to call ffmpeg and concatenate the trimmed videos
concatenate_command = (f"ffmpeg -i 'concat:{input_file_1}|{input_file_2}' "
                       f"-c copy -map 0:v -map 0:a:0 {output_file}")

trim_command_1 = (f"ffmpeg -i {input_file_1} "
                  f"-ss {timestamp_1_start} -to {timestamp_1_end} "
                  f"-c copy -map 0:v -map 0:a:0 trimmed_1.mp4")
trim_command_2 = (f"ffmpeg -i {input_file_2} "
                  f"-ss {timestamp_2_start} -to {timestamp_2_end} "
                  f"-c copy -map 0:v -map 0:a:0 trimmed_2.mp4")

# call subprocess to execute the trim commands
subprocess.run(trim_command_1, shell=True)
subprocess.run(trim_command_2, shell=True)

# call subprocess to execute the concatenate command
subprocess.run(concatenate_command, shell=True)
