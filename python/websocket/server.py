import asyncio
import websockets

PORT = 8765

# List of connected clients
connected = set()


# Create handler for each connection
async def handler(websocket, path):
    try:
        client_name = await websocket.recv()
        connected.add(websocket)
        print(f"{client_name} has connected to the server")

        async for msg in websocket:
            websockets.broadcast(connected, msg)

    except websockets.exceptions.ConnectionClosed:
        connected.remove(websocket)
        print(f"{client_name} has disconnected")


async def main():
    async with websockets.serve(handler, "localhost", PORT):
        print(f"Server started at {PORT}")
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
