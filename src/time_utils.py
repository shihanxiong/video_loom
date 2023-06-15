from datetime import datetime, timedelta


class TimeUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y_%m_%d")

    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    @staticmethod
    def convert_seconds_to_duration(seconds):
        return str(timedelta(seconds=seconds))

    @staticmethod
    def convert_duration_to_seconds(duration):
        time_object = datetime.strptime(duration, "%H:%M:%S")
        time_delta = timedelta(
            hours=time_object.hour,
            minutes=time_object.minute,
            seconds=time_object.second,
        )
        return int(time_delta.total_seconds())
