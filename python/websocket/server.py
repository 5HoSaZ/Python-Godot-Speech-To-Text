import asyncio
import websockets

PORT = 8765

# List of connected clients
connected = set()


# create handler for each connection
async def handler(websocket, path):
    try:
        client_name = await websocket.recv()
        client_name = websocket.remote_address
        connected.add(websocket)
        print(f"{client_name} has connected to the server")

        async for msg in websocket:
            print(f"{client_name}: {msg}")

            for conn in connected:
                if conn != websocket:
                    await conn.send(f"{client_name}: {msg}")

    except websockets.exceptions.ConnectionClosed:
        print(f"{client_name} has disconnected")


start_server = websockets.serve(handler, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
