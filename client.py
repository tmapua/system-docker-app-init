#code for ws client
import asyncio
import subprocess
import threading
import socket
from time import sleep
import websockets

condition = threading.Condition()
flag = 1
message = None
query = None

async def get_weather():
    global condition
    global flag
    global message
    uri = "ws://172.17.0.2:8082" #change to IP address of the server
    while(True):
        async with websockets.connect(uri) as websocket:
            print("Connected to Docker!")
            #action here
            while(True):
                condition.acquire()
                try:
                    if flag == 0:
                        await websocket.send(query)
                        print("Query sent!")
                        query = None
                        message = await websocket.recv()
                        print(message)
                        flag = 1
                        print("flag: {}".format(flag))
                    else:
                        condition.wait()
                    condition.release()
                    condition.notifyAll()
                except:
                    print("Error in connecting to Docker; please check the container's log files.")
                    break


async def weatherapp():
    global condition
    global flag
    global message

    while(True):
        try:
            print("Attempting to connect to cloud...")
            async with websockets.connect("ws://rpkl2.kasilag.me:8080/weather") as websocket:
                print("Connected to S1!")
                while(True):
                    condition.acquire()
                    try:
                        if flag == 1:
                            if message:
                                await websocket.send(message)
                                message = None
                            query = await websocket.recv()
                            flag = 0
                            # print("Sending message...")
                            # await websocket.send(message)
                            # message = None
                            # flag = 0
                        else:
                            condition.wait()
                        condition.release()
                        condition.notifyAll()
                    except websockets.ConnectionClosed:
                        pass
        except:
            pass

def weather():
    weather_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(weather_loop)
    weather_loop.run_until_complete(get_weather())
    weather_loop.run_forever()

def send_to_s1():
    client_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_loop)
    client_loop.run_until_complete(weatherapp())
    client_loop.run_forever()

def docker_cp():
    while True:
        try:
            subprocess.call(['docker', 'cp', 'server_app:/app/ip_addresses.txt', '.'])
        except:
            continue
        sleep(5)

s1_thread = threading.Thread(target=send_to_s1, args=())
weather_thread = threading.Thread(target=weather, args=())
docker_thread = threading.Thread(target=docker_cp, args=())
s1_thread.start()
weather_thread.start()
docker_thread.start()