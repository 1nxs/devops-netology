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

Role Variables
--------------
[./defaults/main.yml](./defaults/main.yml) - предназначен для установки реквизитов подключения - корректируется пользователем

[./vars/main.yml](./vars/main.yml) - содержит переменные необходимые для установки пакетов и конфигурационных файлов

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
