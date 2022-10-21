#!/usr/bin/env python3
#
import datetime
import socket
import time
import json
import yaml

# Нули
service_host = {
    'drive.google.com': '0',
    'mail.google.com': '0',
    'google.com': '0'
}

# Функция заполнения словаря Актуальными IP адресами
def fill_tlist(x):
    for node in x:
        ipaddres = socket.gethostbyname(node)
        x[node] = ipaddres
    return x

# Получаем текущие значения
for host in service_host:
    initial_ip = socket.gethostbyname(host)
    service_host[host] = initial_ip

# запись в формате json \ yaml
def wr_json_yaml(y):
    with open('service_host.json', 'w') as jtmp:
        jtmp.write(str(json.dumps(y)))
    with open('service_hosts.yaml', 'w') as ytmp:
        ytmp.write(yaml.dump(y))
    return

while True:
    # Определяем время для каждого цикла
    dtn = datetime.datetime.now()
    d = dtn.strftime('%H:%M:%S')
    print("-")
    # Перебираем хосты из словаря
    for host in service_host:
        old_ip = service_host[host]
        new_ip = socket.gethostbyname(host)
        # Проверяем значение, если не совпадает то записываем в словарь и ругаемся ошибкой
        if new_ip != old_ip:
            service_host[host] = new_ip
            #print(d+" [ERROR] "+host+" IP changed: old IP "+old_ip+", new IP "+new_ip)
            print(d + " - " +host + " : " +new_ip + " <<< [IP changed] - old IP >>> "+old_ip +"")
            #print("[ERROR] Shit happens at >>>>>>", d)
        print(d + " - "+host + " : " +service_host[host])
        wr_json_yaml(service_host)
    time.sleep(10)