import torch
import numpy as np
import pyaudio
from pyaudio import PyAudio

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paFloat32
CHANNELS = 1


class Recorder(PyAudio):
    sample_rate = 16000

    def record_audio(self) -> torch.Tensor:
        stream = self.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.get_default_input_device_info()["index"],
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

        print("Start recording")

        frames = []
        seconds = 5
        for _ in range(int(self.sample_rate / FRAMES_PER_BUFFER + seconds)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)

        print("Recording stopped")

        stream.stop_stream()
        stream.close()

        # Return normalized float32 array
        res = np.frombuffer(b"".join(frames), dtype=np.float32).reshape(1, -1)
        return torch.tensor(res, device=device)


if __name__ == "__main__":
    rec = Recorder()
    arr = rec.record_audio()
    print(arr)
    rec.terminate()
