import asyncio


class Audio:
    """
    Base Audio class.
    """

    CHANNELS = 1  # Mono
    SAMPLE_RATE = 44100
    CHUNK = 512

    def __init__(self) -> None:
        self.audio_queue = asyncio.Queue()

    async def receive(self):
        """
        Receive audio from source.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_queue(self):
        return self.audio_queue
