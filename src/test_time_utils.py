from time_utils import TimeUtils
from freezegun import freeze_time


@freeze_time("1990-02-08 01:23:45")
def test_get_current_timestamp():
    time_utils = TimeUtils()
    assert time_utils.get_current_timestamp() == '1990_02_08_01_23_45'


@freeze_time("1990-02-08 01:23:45")
def test_get_current_date():
    time_utils = TimeUtils()
    assert time_utils.get_current_date() == '1990_02_08'
