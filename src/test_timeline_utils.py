from timeline_utils import TimelineUtils


def test_parse_timeline_valid():
    timeline_utils = TimelineUtils()
    timeline_text = "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n3,0:00:10,0:00:15"
    assert timeline_utils.parse_timeline(timeline_text) == [
        ['1', '0:00:01', '0:00:05'],
        ['2', '0:00:05', '0:00:10'],
        ['3', '0:00:10', '0:00:15']
    ]


def test_parse_timeline_with_leading_trailing_spaces():
    timeline_utils = TimelineUtils()
    timeline_text = " 1,0:00:01,0:00:05\n2,0:00:05,0:00:10 \n3,0:00:10,0:00:15"
    assert timeline_utils.parse_timeline(timeline_text) == [
        ['1', '0:00:01', '0:00:05'],
        ['2', '0:00:05', '0:00:10'],
        ['3', '0:00:10', '0:00:15']
    ]


def test_parse_timeline_with_spaces_in_middle():
    timeline_utils = TimelineUtils()
    timeline_text = "1,0:00:01, 0:00:05\n2,0:00:05, 0:00:10\n3,0:00:10,0:00:15"
    assert timeline_utils.parse_timeline(timeline_text) == [
        ['1', '0:00:01', '0:00:05'],
        ['2', '0:00:05', '0:00:10'],
        ['3', '0:00:10', '0:00:15']
    ]


def test_parse_timeline_extra_eol():
    timeline_utils = TimelineUtils()
    timeline_text = "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n\n3,0:00:10,0:00:15\n\n\n"
    assert timeline_utils.parse_timeline(timeline_text) == [
        ['1', '0:00:01', '0:00:05'],
        ['2', '0:00:05', '0:00:10'],
        ['3', '0:00:10', '0:00:15']
    ]


def test_validate_timeline():
    timeline_utils = TimelineUtils()

    # when timeline is missing a timestamp
    timeline_text_1 = "1,0:00:01,0:00:05\n2,0:00:10\n3,0:00:10,0:00:15"
    assert timeline_utils.validate_timeline(
        timeline_text_1) == "Missing timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"

    # when timeline has additional element
    timeline_text_2 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:20\n3,0:00:10,0:00:15,0:00:15"
    assert timeline_utils.validate_timeline(
        timeline_text_2) == "Redundant timeline value - ensure the timeline is in format '<video_number>,<start_time>,<end_time>' and separated by comma ','"

    # when timeline start time is equal or after the end time
    timeline_text_3 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:09\n3,0:00:10,0:00:15"
    timeline_text_4 = "1,0:00:01,0:00:05\n2,0:00:10,0:00:10\n3,0:00:10,0:00:15"
    assert timeline_utils.validate_timeline(
        timeline_text_3) == "Invalid timeline - start time is equal/after end time"
    assert timeline_utils.validate_timeline(
        timeline_text_4) == "Invalid timeline - start time is equal/after end time"
