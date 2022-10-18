#!/usr/bin/env python3
from datetime import datetime
import socket
import time

service_host = {
    'drive.google.com': '0',
    'mail.google.com': '0',
    'google.com': '0'
}
for host in service_host:
    initial_ip = socket.gethostbyname(host)
    service_host[host] = initial_ip

while True:
    for host in service_host:
        old_ip = service_host[host]
        new_ip = socket.gethostbyname(host)
        if new_ip != old_ip:
            service_host[host] = new_ip


        print(host + " - " + service_host[host])
    time.sleep(10)