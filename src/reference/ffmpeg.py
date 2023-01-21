# stream = ffmpeg.input(os.path.abspath(self.video_list[0]))
# video = stream.trim(start=5, end=10).filter(
#     "setpts", self.pts_filter)
# video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
# output = ffmpeg.output(
#     video_and_audio, self.output_file_name.get(), format="mp4")
# # TODO: switch to run_async()
# ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
# except ffmpeg.Error as e:
#             print("stdout:", e.stdout.decode("utf8"))
#             print("stderr:", e.stderr.decode('utf8'))
#             raise e
