import asyncio
from typing import Callable


class ASRInterface:
    """
    Common interface for asr transcription.
    """

    async def transcribe(self, audio_queue: asyncio.Queue, callback: Callable = None):
        """
        Transcribe the given audio frame with callback on transcription.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
