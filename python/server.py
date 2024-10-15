import asyncio
import websockets
import numpy as np
import uuid
import os
from asr import ASR_VOSK, ASR_WAV2VEC
from audio import WebsocketAudio, WebSocketAudio_VAD

WebSocketCLient = websockets.WebSocketClientProtocol

HOST = "localhost"
PORT = 8765


# model_path = os.path.abspath("./python/models/vosk-model-en-us-0.22")
# asr = ASR_VOSK(model_path, sample_rate=16000)
asr = ASR_WAV2VEC(sample_rate=16000)

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
    audio = WebSocketAudio_VAD(websocket)
    audio_queue = audio.get_queue()

    async def callback(text):
        await websocket.send(text)

    async def audio_receiver():
        await audio.receive()

    async def audio_process():
        await asr.transcribe(audio_queue, callback=callback)

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
