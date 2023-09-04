class GlobalState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize global data
            cls._instance.data = {
                "video_list": [],
                "intro": None,
                "outro": None,
            }
        return cls._instance
