import os
from pprint import pprint
import re
import subprocess
import threading
from pyowm_app import weatherapp
import websockets
import asyncio



def tcp_dump(filename):
    subprocess.call(['tcpdump', '-i', 'eth0', '-U', '-w', filename])# '|', 'tcpdump', '-r', '-',])


def dump_print(filename):
    while True:
        if os.path.exists(filename):
            line = subprocess.check_output(['tcptrace', '-b', '-n', filename]).decode('utf-8')
            # import pdb; pdb.set_trace()
            ip_addresses = {x for x in re.findall('\s\d+\.\d+\.\d+\.\d+', line)}
            with open('/app/ip_addresses.txt', 'w') as ip:
                for x in ip_addresses:
                    ip.write('{}\n'.format(x))
            # pprint(ip_addresses)

def weather():
    producer_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(producer_loop)
    start_server = websockets.serve(echo, "172.17.0.2", 8080)    
    producer_loop.run_until_complete(start_server)
    producer_loop.run_forever()

async def echo(websocket, path):
    # async for message in websocket:
    #     #action here
    #     await websocket.send(message)
    #     print(message)
    while True:
        message = await websocket.recv()
        await websocket.send(weatherapp(message))


filename = 'tracefile.pcap'

if os.path.exists(filename):
    os.remove(filename)


client = threading.Thread(target=tcp_dump, args=(filename,))
cpu_monitor = threading.Thread(target=dump_print, args=(filename,))#, daemon=True)
weather_app = threading.Thread(target=weather, args=())
client.start()
cpu_monitor.start()
weather_app.start()
