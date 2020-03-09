#code for ws client
import asyncio
import subprocess
import threading
from time import sleep
import websockets

async def get_weather():
    uri = "ws://172.17.0.2:8080" #change to IP address of the server
    async with websockets.connect(uri) as websocket:
        #action here
        while True:
            await websocket.send("weather in manila")
            message = await websocket.recv()
            print(message)

def weather():
    weather_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(weather_loop)
    weather_loop.run_until_complete(get_weather())
    weather_loop.run_forever()

def docker_cp():
    while True:
        try:
            subprocess.call(['docker', 'cp', 'server_app:/app/ip_addresses.txt', '.'])
        except:
            continue
        sleep(5)

weather_thread = threading.Thread(target=weather, args=())
docker_thread = threading.Thread(target=docker_cp, args=())
weather_thread.start()
docker_thread.start()
