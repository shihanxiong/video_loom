from datetime import datetime


class TimeUtils():
    def __init__(self):
        pass

    def get_current_timestamp(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
