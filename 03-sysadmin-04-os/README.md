# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

> Before start:\
> IP: 192.168.87.169/24\
> GW\DNS: 192.168.87.1\
> vlan10: access port >>> no op's needed
1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

- Устанавливаем
```bash
$ cd /opt/ && sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz
$ sudo tar xzf node_exporter-*
$ sudo touch /usr/local/lib/systemd/system/node_exporter.service
```
- Создаем UNIT
```bash
$ sudo nano /usr/local/lib/systemd/system/node_exporter.service
[Unit]
Description="Netology test node_exporer service"

[Service]
EnvironmentFile=/opt/node_exporter-1.2.2.linux-amd64/node_exporter.env
ExecStart=/opt/node_exporter-1.2.2.linux-amd64/node_exporter $EXTRA_OPTS
StandardOutput=file:/var/log/node_explorer.log
StandardError=file:/var/log/node_explorer.log

[Install]
WantedBy=multi-user.target
```
- Прививаем автостарт
```bash
$ sudo systemctl status node_exporter.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable node_exporter.service
```
- Проверка старта по перезагрузке
```bash
$ journalctl -u node_exporter.service
Oct 05 13:55:08 vagrant systemd[1]: Started "Netology test node_exporer service".
Oct 05 13:56:25 vagrant systemd[1]: Stopping "Netology test node_exporer service"...
Oct 05 13:56:25 vagrant systemd[1]: node_exporter.service: Deactivated successfully.
Oct 05 13:56:25 vagrant systemd[1]: Stopped "Netology test node_exporer service".
-- Boot 6f6e0ec964d44f93b7859a77c786601d --
Oct 05 13:56:28 vagrant systemd[1]: Started "Netology teste node_exporer service".
```

- Добавление опций регулируется переменной `$EXTRA_OPTS`:
```bash
$ cat /opt/node_exporter-1.4.0.linux-amd64/node_exporter.env
EXTRA_OPTS="--log.level=info"
```

2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

- из консоли ``curl http://localhost:9100/metrics``
- барузер ``http://192.168.87.169:9100/metrics``

* Для CPU (для каждого из возможных ядер)
```
node_cpu_seconds_total{cpu="0",mode="idle"}
node_cpu_seconds_total{cpu="0",mode="system"}
node_cpu_seconds_total{cpu="0",mode="user"}
process_cpu_seconds_total
```
* Для ОЗУ
```
node_memory_MemAvailable_bytes
node_memory_MemFree_bytes
node_memory_Buffers_bytes
node_memory_Cached_bytes
```
* По дискам (выбрать необходимые диски)
```
node_disk_io_time_seconds_total{device="sda"}
node_disk_read_time_seconds_total{device="sda"}
node_disk_write_time_seconds_total{device="sda"}
node_filesystem_avail_bytes
```
* По сети
```
node_network_info
node_network_receive_bytes_total
node_network_receive_errs_total
node_network_transmit_bytes_total
node_network_transmit_errs_total
```

3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.
- Ставим и настраиваем
```bash
$ sudo apt-get install netdata
$ sudo vi /etc/netdata/netdata.conf
$ sudo systemctl restart netdata.service
$ grep -e bind -e web /etc/netdata/netdata.conf
        web files owner = root
        web files group = root
        bind socket to IP = 0.0.0.0
```
- С ноута заходит, метрики смотрим
```bash
$ sudo tcpdump -nni any port 19999 -c 4
tcpdump: data link type LINUX_SLL2
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
20:07:48.328933 enp0s3 In  IP 192.168.87.253.53773 > 192.168.87.169.19999: Flags [P.], seq 3475084318:3475084740, ack 3380231587, win 513, length 422
20:07:48.329124 enp0s3 Out IP 192.168.87.169.19999 > 192.168.87.253.53773: Flags [P.], seq 1:537, ack 422, win 22904, length 536
20:07:48.368990 enp0s3 In  IP 192.168.87.253.53773 > 192.168.87.169.19999: Flags [.], ack 537, win 511, length 0
20:07:59.326729 enp0s3 In  IP 192.168.87.253.53773 > 192.168.87.169.19999: Flags [P.], seq 422:844, ack 537, win 511, length 422
4 packets captured
9 packets received by filter
0 packets dropped by kernel
```

4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?
Если специально не создают фейки и не скрывают Fingerprint системы, то можно.
```bash
# Инфо о том, что это VirtualBox
$ sudo dmesg | grep -i 'Hypervisor detected'
[    0.000000] Hypervisor detected: KVM
$ sudo dmesg | grep -i 'Virtualization*'
[    2.822689] systemd[1]: Detected virtualization oracle.
```


5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

`man proc` по параметру `/proc/sys/fs/nr_open` отсылает к лимиту RLIMIT_NOFILE в man getrlimit, он определяет максимальное количество файловых дескрипторов, которые может открыть процесс.\
По-умолчанию значение = `1048576`\
Команды `ulimit -Sn` и `ulimit -Hn` отображают soft (данный параметр можно увеличить системным вызовом `setrlimit` до пределов установленных в переменной hard) и hard значение вышеназванного ограничения устанавливаемого на сессионном уровне.\
Дополнительно, параметром `/proc/sys/fs/file-max` устанавливается максимальное ограничение на количество файловых дескрипторов аллоцируемых ядром.

```bash
$ /sbin/sysctl -n fs.nr_open
1048576
$ ulimit -Sn
1024
$ ulimit -Hn
1048576
```

6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.
```bash
$ sudo unshare -f --pid --mount-proc /bin/bash
root@vagrant:/home/vagrant# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.4   7632  4080 pts/1    S    07:22   0:00 /bin/bash
root           7  0.0  0.1  10068  1596 pts/1    R+   07:22   0:00 ps aux
---
root        1602  0.0  0.4   7632  4188 pts/1    S    07:22   0:00 /bin/bash
root        2317  0.0  0.1   5768  1112 pts/1    S+   07:23   0:00 sleep 1h
vagrant     2607  0.0  0.1  10068  1592 pts/2    R+   07:24   0:00 ps aux

$ sudo nsenter --target 2317 --pid --mount
root@vagrant:/home/vagrant# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.4   7632  4188 pts/1    S    07:22   0:00 /bin/bash
root           8  0.0  0.1   5768  1112 pts/1    S+   07:23   0:00 sleep 1h
root           9  0.0  0.5   8656  5452 pts/3    S    07:28   0:00 -bash
root          19  0.0  0.1  10068  1604 pts/3    R+   07:28   0:00 ps aux
```

7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?\
![default_task_pid_max](img/forkbomb.png)
- Линк на [педивикию](https://en.wikipedia.org/wiki/Fork_bomb)
```Bash
# Можно переписать следующим образом:
:(){
 :|:&
};:
# или ещё:
bomb() { 
 bomb | bomb &
}; bomb
```
Данная функция рекурсивно вызывает себя и передается через пайп другому вызову этой же функции (в фоне).
По сути запускаются 2 фоновых процесса, каждый из которых вызывает еще два фоновых процесса и тд, пока не закончатся ресурсы. \

- thread #1  

в файле `/usr/lib/systemd/system/user-.slice.d/10-defaults.conf` можно изменить параметр TasksMax на больший процент, конкретное число или infinity, чтобы убрать лимит совсем.
```bash
vagrant@vagrant:~$ more /usr/lib/systemd/system/user-.slice.d/10-defaults.conf
[Unit]
Description=User Slice of UID %j
Documentation=man:user@.service(5)
After=systemd-user-sessions.service
StopWhenUnneeded=yes

[Slice]
# TasksMax=33%
TasksMax=60%
vagrant@vagrant:~$
```
- thread #2

Максимальное количество процессов для пользователя можно изменить командой `ulimit -u <число>` или в файле cat `etc/security/limits.conf`
```bash
vagrant@vagrant:~$ ulimit -u
3434
vagrant@vagrant:~$ ulimit -u 50
```
Изменить максимальное количество PID можно посредством команд `sysctl -w kernel.pid_max=<число>`,`echo <число> > /proc/sys/kernel/pid_max` или задать переменную `kernel.pid_max` в файле  `/etc/sysctl.conf`

Ограничение на максимальное число процессов на уровне системы установлено в переменной DefaultTasksMax: `systemctl show --property DefaultTasksMax` изменить данную переменную можно в файле `/etc/systemd/system.conf`

Переменная `UserTasksMax` в файле `/etc/systemd/logind.conf` позволяет установить ограничение по максимальному количеству процессов на уровне пользователей 

