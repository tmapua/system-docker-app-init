import os
from pprint import pprint
import re
import subprocess
import threading
from pyowm_app import weatherapp



def tcp_dump(filename):
    subprocess.call(['tcpdump', '-i', 'eth0', '-U', '-w', filename])# '|', 'tcpdump', '-r', '-',])


def dump_print(filename):
    while True:
        if os.path.exists(filename):
            line = subprocess.check_output(['tcptrace', '-b', '-n', filename]).decode('utf-8')
            # import pdb; pdb.set_trace()
            ip_addresses = set(x for x in re.findall('\s\d+\.\d+\.\d+\.\d+', line))
            # pprint(ip_addresses)

def weather():
    while True:
        message = input("query: ")
        with open("weather.txt", "w") as file:
            file.write(weatherapp(message))
        # print(weatherapp(message))


filename = 'lol.pcap'

if os.path.exists(filename):
    os.remove(filename)

client = threading.Thread(target=tcp_dump, args=(filename,))
cpu_monitor = threading.Thread(target=dump_print, args=(filename,))#, daemon=True)
weather_app = threading.Thread(target=weather, args=())
client.start()
cpu_monitor.start()
weather_app.start()
