class GlobalState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {"video_list": []}  # Initialize global data
        return cls._instance
