from datetime import datetime
import random


class TimelineUtils:
    _MISS_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Missing timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _REDUNDANT_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Redundant timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _START_TIME_AFTER_END_TIME_ERROR_MESSAGE = (
        "Invalid timeline - start time is equal/after end time"
    )
    _EMPTY_TIMELINE_ERROR_MESSAGE = "Invalid timeline - timeline cannot be empty"

    def __init__(self):
        pass

    def parse_timeline(self, timeline_text):
        parsed_timeline_arr = []
        for timeline in timeline_text.splitlines():
            if timeline != "":
                video, start, end = timeline.strip().split(",")
                parsed_timeline_arr.append([video.strip(), start.strip(), end.strip()])

        return parsed_timeline_arr

    def validate_timeline(self, timeline_text):
        if timeline_text.replace("\n", "").replace("\t", "").replace(" ", "") == "":
            return self._EMPTY_TIMELINE_ERROR_MESSAGE

        try:
            parsed_timeline_arr = self.parse_timeline(timeline_text)

            for idx, parsed_timeline in enumerate(parsed_timeline_arr):
                video, start, end = parsed_timeline
                start_in_time = datetime.strptime(start, "%H:%M:%S").time()
                end_in_time = datetime.strptime(end, "%H:%M:%S").time()

                if start_in_time >= end_in_time:
                    return self._START_TIME_AFTER_END_TIME_ERROR_MESSAGE
        except ValueError as e:
            if "not enough values to unpack" in str(e):
                return self._MISS_VALUE_IN_TIMELINE_ERROR_MESSAGE
            elif "too many values to unpack" in str(e):
                return self._REDUNDANT_VALUE_IN_TIMELINE_ERROR_MESSAGE
            else:
                return e

        return None

    @staticmethod
    def generate_random_segments(num_segments, minutes_per_segment, num_videos):
        for i in range(num_segments + 1):
            print(i)

    @staticmethod
    def generate_next_video_num(num_video, prev):
        num = random.randint(1, num_video)

        if num == prev:
            TimelineUtils.generate_next_video_num(num_video=num_video, prev=prev)
        else:
            return num

    @staticmethod
    def generate_next_segment_time(minutes_per_segment, prev):
        margin = random.randint(-30, 30)
