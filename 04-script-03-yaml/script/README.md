### [Задание 2](04-yaml-task-02.py)
```python
#!/usr/bin/env python3
#
from datetime import datetime
import socket
import time

# Нули
service_host = {
    'drive.google.com': '0',
    'mail.google.com': '0',
    'google.com': '0'
}
# Получаем текущие значения
for host in service_host:
    initial_ip = socket.gethostbyname(host)
    service_host[host] = initial_ip

while True:
    # Пишем время старта цикла
    dt = datetime.now()
    print("'-..-''-..-'  ", dt)
    # Перебираем хосты из словаря
    for host in service_host:
        old_ip = service_host[host]
        new_ip = socket.gethostbyname(host)
        # Проверяем значение, если не совпадает то записываем в словарь и ругаемся ошибкой
        if new_ip != old_ip:
            service_host[host] = new_ip
            print("[ERROR] "+host+" IP changed: old IP "+old_ip+", new IP "+new_ip)
            print("[ERROR] Shit happens at >>>>>>", dt)
        print(host + " - " + service_host[host])
    time.sleep(10)
```
- вывод теста:<br>
[]()