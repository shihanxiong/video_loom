from datetime import datetime


class TimelineUtils():
    _MISS_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Missing timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _REDUNDANT_VALUE_IN_TIMELINE_ERROR_MESSAGE = "Redundant timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    _START_TIME_AFTER_END_TIME_ERROR_MESSAGE = "Invalid timeline - start time is equal/after end time"

    def __init__(self):
        pass

    def parse_timeline(self, timeline_text):
        parsed_timeline_arr = []
        for timeline in timeline_text.splitlines():
            if timeline != "":
                video, start, end = timeline.strip().split(",")
                parsed_timeline_arr.append(
                    [video.strip(), start.strip(), end.strip()])

        return parsed_timeline_arr

    def validate_timeline(self, timeline_text):
        try:
            parsed_timeline_arr = self.parse_timeline(timeline_text)

            for idx, parsed_timeline in enumerate(parsed_timeline_arr):
                video, start, end = parsed_timeline
                start_in_time = datetime.strptime(start, '%H:%M:%S').time()
                end_in_time = datetime.strptime(end, '%H:%M:%S').time()

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
