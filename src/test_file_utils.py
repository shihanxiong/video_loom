import re
from file_utils import FileUtils


def test_escape_file_name():
    file_utils = FileUtils()
    assert file_utils.escape_file_name("abc.mp4") == "\"abc.mp4\""


def test_get_latest_version_from_changelog():
    file_utils = FileUtils()
    assert bool(re.match('^[v][0-9][.][0-9][.][0-9]$', file_utils.get_latest_version_from_changelog())
                ) or file_utils.get_latest_version_from_changelog() == 'unreleased' or file_utils.get_latest_version_from_changelog() == 'Hackday'
