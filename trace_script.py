import os
from pprint import pprint
import re
import subprocess
import threading



def tcp_dump(filename):
    subprocess.call(['tcpdump', '-i', 'eth0', '-U', '-w', filename])# '|', 'tcpdump', '-r', '-',])


def dump_print(filename):
    while True:
        if os.path.exists(filename):
            line = subprocess.check_output(['tcptrace', '-b', '-n', filename])
            ip_addresses = set(x for x in re.findall("\s\d+\.\d+\.\d+\.\d+", line))
            # pprint(ip_addresses)
            print(len(ip_addresses))


filename = 'lol.pcap'

if os.path.exists(filename):
    os.remove(filename)

client = threading.Thread(target=tcp_dump, args=(filename,))
cpu_monitor = threading.Thread(target=dump_print, args=(filename,))#, daemon=True)
client.start()
cpu_monitor.start()
