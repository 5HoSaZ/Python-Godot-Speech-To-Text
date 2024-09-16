import asyncio
import websockets


IP = "localhost"
PORT = 8765

# List of connected clients
connected = set()


# def write_to_wav(bytes, filename="myfile.ogg"):
#     with wave.open(filename, "wb") as wf:
#         wf.setnchannels(1)  # mono
#         wf.setsampwidth(2)  # 1 bytes per sample
#         wf.setframerate(44100)
#         wf.writeframes(bytes)


# Create handler for each connection
async def handler(websocket, path):
    try:
        connected.add(websocket)
        print("A client has connected")

        async for msg in websocket:
            print(f"Message from client: {msg}")
            await websocket.send(f"Got your message: {msg}")

    except websockets.exceptions.ConnectionClosed as e:
        print(e)

    finally:
        print("disconnected")
        connected.remove(websocket)


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        print(f"Server started at {PORT}")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
