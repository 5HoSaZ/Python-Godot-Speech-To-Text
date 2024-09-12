import asyncio
import websockets


async def listen():
    url = "ws://localhost:8765"

    async with websockets.connect(url) as websocket:
        name = input("What's your name: ")
        await websocket.send(name)
        print(f"Client's name: {name}")

        # Send a message to the server
        await websocket.send("Hello server!")

        # Listen
        while True:
            msg = await websocket.recv()
            print(msg)


asyncio.get_event_loop().run_until_complete(listen())
