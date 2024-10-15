from .asr_interface import ASRInterface

import asyncio
import numpy as np
import torch
import torchaudio
from torchaudio.functional import resample

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])


class ASR_WAV2VEC(ASRInterface):
    """Wav2Vec pcm16"""

    def __init__(self, sample_rate):
        self.bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
        self.model = self.bundle.get_model().to(DEVICE)
        self.decoder = GreedyCTCDecoder(labels=self.bundle.get_labels())
        self.sample_rate = sample_rate
        print("Model loaded")

    async def transcribe(self, audio_queue: asyncio.Queue):
        frame = b""
        duration = 0
        while True:
            next_frame = await audio_queue.get()
            if next_frame == "stop":
                break
            frame_duration = len(next_frame) / 2 / self.sample_rate
            frame += next_frame
            duration += frame_duration
            if duration < 2:
                continue
            frame = (
                np.frombuffer(frame, dtype=np.int16).astype(dtype=np.float32) / 32768
            )
            frame = frame.reshape(1, -1)
            frame = torch.tensor(frame)
            if self.sample_rate != self.bundle.sample_rate:
                frame = resample(frame, self.sample_rate, self.bundle.sample_rate)
            with torch.inference_mode():
                emission, _ = self.model(frame)
            transcript = self.decoder(emission[0])
            print(f"Recognized: {transcript}")
            frame = b""
            duration = 0
