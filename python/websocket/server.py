import asyncio
import websockets
import numpy as np
import uuid
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

WebSocketCLient = websockets.WebSocketClientProtocol

CHUNK = 512
RATE = 44100
HOST = "localhost"
PORT = 8765

# model_path = os.path.abspath("./python/models/vosk-model-en-us-0.22")
# recase_path = os.path.abspath("./python/models/vosk-recasepunc-en-0.22/recasepunc.py")
# recase_ckpt = os.path.abspath("./python/models/vosk-recasepunc-en-0.22/checkpoint")

# model = Model(model_path=model_path)
# rec = KaldiRecognizer(model, RATE)
# print("Model loaded")

p = pyaudio.PyAudio()
player = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK,
)


# List of connected clients
connected = dict()


# Create handler for each connections
async def handler(websocket: WebSocketCLient, path: str):
    try:
        client_id = uuid.uuid4()
        connected[client_id] = websocket
        print(f"Client {client_id} has connected")
        await audio_channel(websocket)
    except websockets.exceptions.ConnectionClosed as e:
        print(e)
    finally:
        del connected[client_id]
        print(f"Client {client_id} has disconnected")


async def audio_channel(websocket: WebSocketCLient):
    audio_queue = asyncio.Queue()

    async def audio_receiver():
        print("Listening...")
        async for frames in websocket:
            # Audio frames should be a byte of int16
            audio_queue.put_nowait(frames[8:])
        audio_queue.put_nowait(None)

    async def audio_process():
        while True:
            data = await audio_queue.get()
            if data is None:
                break
            # if rec.AcceptWaveform(data):
            #     result = rec.Result()
            #     text = json.loads(result)["text"]
            #     print(f"Recognized: {text}")
            # else:
            #     partial_result = rec.PartialResult()
            #     print(f"Partial: {json.loads(partial_result)['partial']}")
            #     await websocket.send(
            #         f"Partial: {json.loads(partial_result)['partial']}"
            #     )
            data = np.frombuffer(data, dtype=np.int16)
            player.write(data, CHUNK)

    await asyncio.gather(audio_receiver(), audio_process())


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Server started at {PORT}")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Terminating...")
