Vector role
=========
Роль для установки Vector
- Установка vector и создание system unit
- Установка конфигурации сервиса на передачу данных в clickhouse

Requirements
------------
- Хост на Ubuntu или Debian

Role Variables
--------------
- [./defaults/main.yml](./defaults/main.yml) - предназначен для установки реквизитов подключения
- [./vars/main.yml](./vars/main.yml) - содержит переменные необходимые для установки пакетов и конфигурационных файлов

| Переменная                   | Назначение                                                        |
|:-----------------------------|:------------------------------------------------------------------|
| `vector_distro_version`      | версия `Vector`                                                   |
| `vector_distro.path`         | URL адрес для скачивания пакетов `Vector`                         |
| `vector_distro.package`      | имя установочного пакета `Vector`                                 |
| `vector_config_path`         | каталог файлов конфигурации                                       |

Dependencies
------------

Необходима роль [clickhouse-role](../clickhouse-role)

В inventory должен быть хост `clickhouse-host`
```yaml
---
  clickhouse:
    hosts:
      clickhouse-host:
        ansible_host: IPv4 Address
```
[main.yml](vars%2Fmain.yml) > `endpoint:` - используется при создании конфигурации сервиса

Example Playbook
----------------

```yaml
hosts: vector
roles:
  - role: vector-role
```

License
-------
MIT

Author Information
------------------
- author: Pavel Yakushin
- company: Netology workshop
