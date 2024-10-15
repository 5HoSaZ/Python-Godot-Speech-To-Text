from .audio import Audio


import websockets


class WebsocketAudio(Audio):
    def __init__(self, client: websockets.WebSocketClientProtocol):
        super().__init__()
        self.ws = client

    async def receive(self):
        async for frame in self.ws:
            self.audio_queue.put_nowait(frame[8:])
        self.audio_queue.put_nowait("stop")
