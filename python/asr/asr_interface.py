import asyncio


class ASRInterface:
    """
    Common interface for asr transcription.
    """

    async def transcribe(self, audio_queue: asyncio.Queue):
        """
        Transcribe the given audio frame.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
