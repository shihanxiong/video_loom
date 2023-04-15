from datetime import datetime


class TimeUtils():
    def __init__(self):
        pass

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y_%m_%d")

    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
