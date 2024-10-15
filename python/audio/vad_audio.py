from .audio import Audio

from typing import Iterable
import websockets
import webrtcvad
import librosa
import numpy as np
from collections import deque
import asyncio
import wave


class BytesStream:
    def __init__(self) -> None:
        self.buffer = deque()

    def write(self, bytes: Iterable[bytes]) -> None:
        self.buffer.extend(bytes)

    def read(self, n: int = -1):
        if n < 0:
            n = len(self.buffer)
        return b"".join([self.buffer.popleft().to_bytes(1) for _ in range(n)])

    def clear(self):
        self.buffer.clear()

    def __len__(self):
        return len(self.buffer)


class RingBuffer:
    def __init__(self, maxlen, ratio) -> None:
        self.buffer = deque(maxlen=maxlen)
        self.threshold = int(maxlen * ratio)
        self.triggered = False
        self.out_frame = b""

    def accept(self, frame: bytes, state: bool):
        self.buffer.append((frame, state))
        if self.triggered is False:
            voiced = sum([s for _, s in self.buffer])
            if voiced > self.threshold:
                self.triggered = True
                self.out_frame += b"".join([f for f, _ in self.buffer])
        else:
            self.out_frame += frame
            unvoiced = sum([1 - s for _, s in self.buffer])
            if unvoiced > self.threshold:
                self.triggered = False
                self.buffer.clear()
                out_bytes = self.out_frame
                self.out_frame = b""
                return out_bytes
        return None


def resample_bytes(frame: bytes, in_rate, out_rate):
    frame = np.frombuffer(frame, np.int16) / 32768
    frame = librosa.resample(frame, orig_sr=in_rate, target_sr=out_rate)
    frame = np.array(frame * 32768, dtype=np.int16)
    return frame.tobytes()


class WebSocketAudio_VAD(Audio):
    """
    Audio class implemented Voice Activity Detection on other Audio class.
    """

    def __init__(
        self,
        client: websockets.WebSocketClientProtocol,
        padding_ms: int = 300,
        vad_ms: int = 30,
        ratio: float = 0.75,
    ) -> None:

        super().__init__()
        self.ws = client
        self.vad = webrtcvad.Vad(1)
        self.padding_ms = padding_ms
        self.vad_ms = vad_ms
        self.stream = BytesStream()
        self.ring_buffer = RingBuffer(
            maxlen=int(padding_ms / vad_ms),
            ratio=ratio,
        )

    async def receive(self):
        with wave.open("output.wav", mode="wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            frame_length = 2 * int(16 * self.vad_ms)
            async for frame in self.ws:
                if frame == "stop":
                    break
                next_frame = frame[8:]
                # Rate: 44100 -> 16000
                next_frame = resample_bytes(next_frame, self.SAMPLE_RATE, 16000)
                self.stream.write(next_frame)
                # VAD every 480 frame (960 bytes PCM16)
                while len(self.stream) >= frame_length:
                    frame = self.stream.read(frame_length)
                    is_speech = self.vad.is_speech(frame, 16000)
                    res = self.ring_buffer.accept(frame, is_speech)
                    if res:
                        self.audio_queue.put_nowait(res)
                        wav_file.writeframes(res)
            self.audio_queue.put_nowait("stop")
