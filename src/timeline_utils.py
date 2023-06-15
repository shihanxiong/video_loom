import datetime
import random
from time_utils import TimeUtils


class TimelineUtils:
    _MISS_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Missing timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _REDUNDANT_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Redundant timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _START_TIME_AFTER_END_TIME_ERROR_MESSAGE = (
        "Invalid timeline - start time is equal/after end time"
    )
    _EMPTY_TIMELINE_ERROR_MESSAGE = "Invalid timeline - timeline cannot be empty"
    _END_TIME_EXCEEDS_VIDEO_DURATION_ERROR_MESSAGE = (
        "Invalid timeline - end time exceeds video duration"
    )

    def __init__(self):
        pass

    @staticmethod
    def parse_timeline(timeline_text):
        parsed_timeline_arr = []
        for timeline in timeline_text.splitlines():
            if timeline != "":
                video, start, end = timeline.strip().split(",")
                parsed_timeline_arr.append([video.strip(), start.strip(), end.strip()])

        return parsed_timeline_arr

    @staticmethod
    def validate_timeline(timeline_text, video_durations):
        if timeline_text.replace("\n", "").replace("\t", "").replace(" ", "") == "":
            return TimelineUtils._EMPTY_TIMELINE_ERROR_MESSAGE

        try:
            parsed_timeline_arr = TimelineUtils.parse_timeline(timeline_text)

            for idx, parsed_timeline in enumerate(parsed_timeline_arr):
                video, start, end = parsed_timeline
                start_time = TimeUtils.convert_duration_to_seconds(start)
                end_time = TimeUtils.convert_duration_to_seconds(end)

                if start_time >= end_time:
                    return TimelineUtils._START_TIME_AFTER_END_TIME_ERROR_MESSAGE
                elif end_time > video_durations[int(video)]:
                    return TimelineUtils._END_TIME_EXCEEDS_VIDEO_DURATION_ERROR_MESSAGE
        except ValueError as e:
            if "not enough values to unpack" in str(e):
                return TimelineUtils._MISS_VALUE_IN_TIMELINE_ERROR_MESSAGE
            elif "too many values to unpack" in str(e):
                return TimelineUtils._REDUNDANT_VALUE_IN_TIMELINE_ERROR_MESSAGE
            else:
                return e

        return None

    @staticmethod
    def generate_random_segments(num_segments, min_per_segment, num_videos):
        prev = None
        start = "0:00:00"
        end = 0
        result = ""

        for i in range(num_segments):
            next_video_num = TimelineUtils.generate_next_video_num(
                num_videos=num_videos, prev=prev
            )
            end = str(
                datetime.timedelta(
                    seconds=round(
                        TimelineUtils.generate_next_segment_time(
                            min_per_segment=min_per_segment,
                            prev_in_min=(i * min_per_segment),
                        )
                    )
                )
            )

            result += f"{next_video_num},{start},{end}\n"

            prev = next_video_num
            start = end

        return result

    @staticmethod
    def generate_next_video_num(num_videos, prev):
        num = random.randint(1, num_videos)

        if num == prev:
            return TimelineUtils.generate_next_video_num(
                num_videos=num_videos, prev=prev
            )
        else:
            return num

    @staticmethod
    def generate_next_segment_time(min_per_segment, prev_in_min):
        margin_in_sec = random.randint(-30, 30)
        return (prev_in_min + min_per_segment) * 60 + margin_in_sec

    @staticmethod
    def generate_youtube_timestamp(timeline_text, labels):
        parsed_timeline_arr = TimelineUtils.parse_timeline(timeline_text)
        youtube_timestamp = ""
        for timeline in parsed_timeline_arr:
            label = labels[int(timeline[0]) - 1]
            youtube_timestamp += f"{timeline[1]} {label}\n"
        return youtube_timestamp
