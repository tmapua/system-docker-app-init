import asyncio
import subprocess
import threading
import socket
from time import sleep
import websockets

async def echo():
    uri = "ws://rpkl2.kasilag.me:8080/weather"
    async with websockets.connect(uri) as websocket:
        while(True):
            message = await websocket.recv()
            await websocket.send("The weather in Manila today is mostly sunny.")

producer = asyncio.get_event_loop()
producer.run_until_complete(echo())
producer.run_forever()