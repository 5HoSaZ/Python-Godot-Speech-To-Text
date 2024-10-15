from .audio import Audio

import asyncio


class VADAudio(Audio):
    """
    Audio class implemented Voice Activity Detection on other Audio class.
    """

    def __init__(self, source: Audio, vad) -> None:
        self.source = source
        self.vad = vad

    async def receive(self):
        pass
