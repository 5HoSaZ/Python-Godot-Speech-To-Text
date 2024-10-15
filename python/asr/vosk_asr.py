from .asr_interface import ASRInterface

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

    async def transcribe(self, audio_queue: asyncio.Queue):
        while True:
            frame: bytes | None = await audio_queue.get()
            if frame is None:
                break
            if self.rec.AcceptWaveform(frame):
                result = self.rec.Result()
                text = json.loads(result)["text"]
                print(f"Recognized: {text}")
