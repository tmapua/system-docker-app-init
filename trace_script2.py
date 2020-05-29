import os
from pprint import pprint
import re
import subprocess
import threading
from pyowm_app import weatherapp
import websockets
import asyncio
import urllib.request



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

async def weather():
    # async for message in websocket:
    #     #action here
    #     await websocket.send(message)
    #     print(message)
    while True:
        ip_address = "13.58.40.196"
        async with websockets.connect("ws:/{}:8080/weather".format(ip_address)) as websocket:
            for message in websocket:
                await websocket.send(weatherapp(message))

async def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def run_client():
    client_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_loop)
    client_loop.run_until_complete(weather)

filename = 'tracefile.pcap'

if os.path.exists(filename):
    os.remove(filename)


# client = threading.Thread(target=tcp_dump, args=(filename,))
# cpu_monitor = threading.Thread(target=dump_print, args=(filename,))#, daemon=True)
weather_app = threading.Thread(target=run_client, args=())
client.start()
cpu_monitor.start()
weather_app.start()
