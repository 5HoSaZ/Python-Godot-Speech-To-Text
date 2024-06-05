import torch
import torchaudio
from modules.voice_input import Recorder


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


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().to(device)
decoder = GreedyCTCDecoder(labels=bundle.get_labels())


if __name__ == "__main__":
    rec = Recorder()
    res = rec.record_audio()
    rec.terminate()
    waveform, sample_rate = torch.tensor(res), 16000
    waveform = waveform.to(device)
    print(waveform)

    with torch.inference_mode():
        emission, _ = model(waveform)

    transcript = decoder(emission[0])
    print(transcript)
