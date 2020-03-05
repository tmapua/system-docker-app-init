#code for ws client
import asyncio
import websockets

async def hello():
    uri = "ws://172.17.0.2:8080" #change to IP address of the server
    async with websockets.connect(uri) as websocket:
        #action here
        await websocket.send("weather in manila")
        message = await websocket.recv()
        print(message)

asyncio.get_event_loop().run_until_complete(hello())
