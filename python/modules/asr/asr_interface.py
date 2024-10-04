class ASRInterface:
    async def transcribe(self, client):
        """
        Transcribe the given audio data.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
