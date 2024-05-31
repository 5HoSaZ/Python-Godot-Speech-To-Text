import numpy as np
import pyaudio
from pyaudio import PyAudio

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


class Recorder(PyAudio):
    def record_audio(self) -> np.ndarray:
        stream = self.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=self.get_default_input_device_info()["index"],
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

        print("Start recording")

        frames = []
        seconds = 5
        for _ in range(int(RATE / FRAMES_PER_BUFFER + seconds)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)

        print("Recording stopped")

        stream.stop_stream()
        stream.close()

        return np.frombuffer(b"".join(frames), dtype="int16")


if __name__ == "__main__":
    rec = Recorder()
    arr = rec.record_audio()
    print(arr)
    rec.terminate()
