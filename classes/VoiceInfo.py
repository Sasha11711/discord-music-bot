class VoiceInfo:
    def __init__(self):
        self.queue: dict[str, list[dict]] = []
        self.skip_votes = []
        self.is_repeating = False
        self.song_start_time = None