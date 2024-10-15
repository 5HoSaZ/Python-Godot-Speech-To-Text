from .audio import Audio

import asyncio
import pyaudio


class MicAudio(Audio):
    def __init__(self):
        super().__init__()
        self.p = pyaudio.PyAudio()
        # chunk = int(RATE * VAD_DURATION)
        self.stream = self.p.open(
            input=True,
            format=pyaudio.paInt16,
            channels=Audio.CHANNELS,
            rate=Audio.SAMPLE_RATE,
            frames_per_buffer=512,
            stream_callback=self.callback,
        )

    def callback(self, in_data, frame_count, time_info, status):
        self.audio_queue.put_nowait(in_data)
        return None, pyaudio.paContinue

    async def __aexit__(self, type, value, traceback):
        self.audio_queue.put_nowait("stop")
        await self.close()

    async def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    async def receive(self):
        self.stream.start_stream()
        while self.stream.is_active():
            await asyncio.sleep(0)
