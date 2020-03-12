#code for ws client
import asyncio
import subprocess
import threading
import sockets
from time import sleep
import websockets

condition = threading.Condition()
flag = 0
message = None

async def get_weather():
    global condition
    global flag
    global message
    uri = "ws://172.17.0.2:8080" #change to IP address of the server
    async with websockets.connect(uri) as websocket:
        #action here
        while True:
            try:
                if flag == 0:
                    async for query in websocket:
                        await websocket.send(query)
                        message = await websocket.recv()
                        print(message)
                        flag = 1
                        print("flag: {}".format(flag))
                else:
                    condition.wait()
                condition.release()
            except:
                print("Error in connecting to Docker; please check the container's log files.")


async def weatherapp(websocket, path):
    global condition
    global flag
    global message

    while(True):
        try:
            if flag == 1:
                print("Sending message...")
                websocket.sent(message)
                flag = 0
            else:
                condition.wait()
            condition.release()
        except websockets.ConnectionClosed:
            pass
        finally:
            print("connection removed")
            break

def weather():
    weather_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(weather_loop)
    weather_loop.run_until_complete(get_weather())
    weather_loop.run_forever()

def send_to_s1():
    producer_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(producer_loop)    
    start_server = websockets.serve(weatherapp, socket.gethostbyname(socket.gethostname()), 8080)
    producer_loop.run_until_complete(start_server)
    producer_loop.run_forever()

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
