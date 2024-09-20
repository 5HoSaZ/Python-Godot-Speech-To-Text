import asyncio
import websockets
import pyaudio
import numpy as np

WebSocketCLient = websockets.WebSocketClientProtocol

CHUNK = 512
RATE = 44100
HOST = "localhost"
PORT = 8765

p = pyaudio.PyAudio()

player = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=RATE,
    output=True,
    frames_per_buffer=10,
)

# List of connected clients
connected = set()


# Create handler for each connections
async def handler(websocket: WebSocketCLient, path: str):
    try:
        connected.add(websocket)
        print("A client has connected")
        await audio_channel(websocket)
    except websockets.exceptions.ConnectionClosed as e:
        print(e)
    finally:
        print("disconnected")
        connected.remove(websocket)


async def audio_channel(websocket: WebSocketCLient):
    audio_queue = asyncio.Queue()

    async def audio_receiver():
        async for frames in websocket:
            # Audio frames should be a byte of float32
            frames = np.frombuffer(frames, dtype=np.float32, offset=8)
            audio_queue.put_nowait(frames)
        audio_queue.put_nowait(None)

    async def audio_process():
        while True:
            data = await audio_queue.get()
            if data is None:
                break
            player.write(data, CHUNK)
            print(data)
        print("Done")

    await asyncio.gather(audio_receiver(), audio_process())


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Server started at {PORT}")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
