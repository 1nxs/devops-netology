Clickhouse role
=========
Роль для установки clickhouse.
- Установка:
  - clickhouse-client
  - clickhouse-server
  - clickhouse-common-static
- Сlickhouse-server конфигурируется для работы внешних подключений
- БД
  - Создаётся БД
  - Создаётся таблица для логов
  - Создаётся пользователь для записи в БД

Requirements
------------
- Хост на CentOS версии 7 или 8

Role Variables
--------------
- [./defaults/main.yml](./defaults/main.yml) - предназначен для установки реквизитов подключения
- [./vars/main.yml](./vars/main.yml) - содержит переменные необходимые для установки пакетов и конфигурационных файлов

| Переменная                   | Назначение                                                        |
|:-----------------------------|:------------------------------------------------------------------|
| `clickhouse_version`         | версия `Clickhouse`                                               |
| `main_package_path.path`     | основной URL адрес для скачивания пакетов `Clickhouse`            |
| `rescue_package_path.path`   | URL адрес пакетов `Clickhouse`, используется при сбое таски       |
| `clickhouse_packages_noarch` | пакеты для установки `Clickhouse`, без зависимости от архитектуры |
| `clickhouse_packages`        | `RPM` пакеты для установки `Clickhouse`                           |

Dependencies
------------
Нет зависимостей

Example Playbook
----------------
```yaml
hosts: clickhouse
roles:
  - role: clickhouse-role
```

License
-------
MIT

Author Information
------------------
- author: Pavel Yakushin
- company: Netology workshop
