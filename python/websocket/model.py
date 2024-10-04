import os
import sys
import wave
import json
import pyaudio
from vosk import Model, KaldiRecognizer

model_path = os.path.abspath("./python/models/vosk-model-en-us-0.22")
recase_path = os.path.abspath("./python/models/vosk-recasepunc-en-0.22/recasepunc.py")
recase_ckpt = os.path.abspath("./python/models/vosk-recasepunc-en-0.22/checkpoint")

model = Model(model_path=model_path)
rec = KaldiRecognizer(model, 16000)
# rec.SetWords(True)

# Load the Vosk model
if not os.path.exists(model_path):
    print(f"Model path '{model_path}' does not exist")
    sys.exit(1)


# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192
)
stream.start_stream()

print("Listening...")

try:
    while True:
        data = stream.read(4096)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result)["text"]
            print(f"Recognized: {text}")
        else:
            partial_result = rec.PartialResult()
            print(f"Partial: {json.loads(partial_result)['partial']}")
except KeyboardInterrupt:
    print("Terminating...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
