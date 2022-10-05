# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

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



4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?



5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?



6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.



7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

