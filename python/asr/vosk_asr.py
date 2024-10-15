from .asr_interface import ASRInterface

from typing import Callable
import json
import asyncio
from vosk import Model, KaldiRecognizer


class ASR_VOSK(ASRInterface):

    def __init__(
        self,
        model_path: str | None = None,
        model_name: str | None = None,
        sample_rate: int | None = None,
    ):
        print("Loading model")
        self.model = Model(model_path, model_name)
        self.rec = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate
        print("Model loaded")

    async def transcribe(self, audio_queue: asyncio.Queue, callback: Callable = None):
        while True:
            frame = await audio_queue.get()
            if frame == "stop":
                break
            if self.rec.AcceptWaveform(frame):
                result = self.rec.Result()
                text = json.loads(result)["text"]
                if callback is None:
                    print(f"Recognized: {text}")
                else:
                    await callback(text)
