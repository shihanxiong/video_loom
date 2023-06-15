from timeline_utils import TimelineUtils

video_durations = {1: 100, 2: 200, 3: 300}


def test_parse_timeline_valid():
    timeline_text = "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n3,0:00:10,0:00:15"
    assert TimelineUtils.parse_timeline(timeline_text) == [
        ["1", "0:00:01", "0:00:05"],
        ["2", "0:00:05", "0:00:10"],
        ["3", "0:00:10", "0:00:15"],
    ]


def test_parse_timeline_with_leading_trailing_spaces():
    timeline_text = " 1,0:00:01,0:00:05\n2,0:00:05,0:00:10 \n3,0:00:10,0:00:15"
    assert TimelineUtils.parse_timeline(timeline_text) == [
        ["1", "0:00:01", "0:00:05"],
        ["2", "0:00:05", "0:00:10"],
        ["3", "0:00:10", "0:00:15"],
    ]


def test_parse_timeline_with_spaces_in_middle():
    timeline_text = "1,0:00:01, 0:00:05\n2,0:00:05, 0:00:10\n3,0:00:10,0:00:15"
    assert TimelineUtils.parse_timeline(timeline_text) == [
        ["1", "0:00:01", "0:00:05"],
        ["2", "0:00:05", "0:00:10"],
        ["3", "0:00:10", "0:00:15"],
    ]


def test_parse_timeline_extra_eol():
    timeline_text = "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n\n3,0:00:10,0:00:15\n\n\n"
    assert TimelineUtils.parse_timeline(timeline_text) == [
        ["1", "0:00:01", "0:00:05"],
        ["2", "0:00:05", "0:00:10"],
        ["3", "0:00:10", "0:00:15"],
    ]


def test_validate_timeline_empty():
    timeline_text = " \n \n\n   \n\n\n"
    assert (
        TimelineUtils.validate_timeline(timeline_text, video_durations)
        == "Invalid timeline - timeline cannot be empty"
    )


def test_validate_timeline():
    # when timeline is missing a timestamp
    timeline_text_1 = "1,0:00:01,0:00:05\n2,0:00:10\n3,0:00:10,0:00:15"
    assert (
        TimelineUtils.validate_timeline(timeline_text_1, video_durations)
        == "Missing timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    )

    # when timeline has additional element
    timeline_text_2 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:20\n3,0:00:10,0:00:15,0:00:15"
    assert (
        TimelineUtils.validate_timeline(timeline_text_2, video_durations)
        == "Redundant timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"
    )

    # when timeline start time is equal or after the end time
    timeline_text_3 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:09\n3,0:00:10,0:00:15"
    timeline_text_4 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:10\n3,0:00:10,0:00:15"
    assert (
        TimelineUtils.validate_timeline(timeline_text_3, video_durations)
        == "Invalid timeline - start time is equal/after end time"
    )
    assert (
        TimelineUtils.validate_timeline(timeline_text_4, video_durations)
        == "Invalid timeline - start time is equal/after end time"
    )

    # when timeline end time exceeds video duration
    timeline_text_5 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:19\n3,0:00:10,0:05:15"
    assert (
        TimelineUtils.validate_timeline(timeline_text_5, video_durations)
        == "Invalid timeline - end time exceeds video duration"
    )


def test_generate_random_segments():
    random_sengments_text = TimelineUtils.generate_random_segments(
        num_segments=10, min_per_segment=3, num_videos=3
    )
    lines = random_sengments_text.splitlines()
    assert len(lines) == 10
    for i in range(1, 10):
        assert lines[i].split(",")[0] != lines[i - 1].split(",")[0]


def test_generate_next_video_num():
    num_videos = 3
    prev = 2
    num = TimelineUtils.generate_next_video_num(num_videos=num_videos, prev=prev)
    assert num != prev
    prev = num
    num = TimelineUtils.generate_next_video_num(num_videos=num_videos, prev=prev)
    assert num != prev
    prev = num
    num = TimelineUtils.generate_next_video_num(num_videos=num_videos, prev=prev)
    assert num != prev


def test_generate_next_segment_time():
    next_segment_time = TimelineUtils.generate_next_segment_time(3, 6)
    assert next_segment_time > (3 + 6 - 1) * 60
    assert next_segment_time < (3 + 6 + 1) * 60


def test_generate_youtube_timestamp():
    timeline_text = "1,0:00:01,0:00:05\n2,0:00:10,0:00:15\n3,0:00:15,0:00:20"
    assert (
        TimelineUtils.generate_youtube_timestamp(
            timeline_text, ["Dan", "Hank", "Lindsay"]
        )
        == "0:00:01 Dan\n0:00:10 Hank\n0:00:15 Lindsay\n"
    )
