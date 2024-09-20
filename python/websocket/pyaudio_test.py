import pyaudio
import numpy as np

CHUNK = 512
RATE = 44100
LEN = 1

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

player = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK,
)

datas = []

print("Start recording")
for i in range(int(LEN * RATE / CHUNK)):  # go for a LEN seconds
    raw = stream.read(CHUNK)
    data = np.frombuffer(raw, dtype=np.int16)
    print(data)
    datas.append(data)


for i in range(int(LEN * RATE / CHUNK)):
    player.write(datas[i], CHUNK)

stream.stop_stream()
stream.close()
p.terminate()
