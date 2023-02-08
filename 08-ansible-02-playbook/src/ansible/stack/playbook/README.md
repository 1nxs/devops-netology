# Описание плейбука site.yml

Предназначен для базового развёртывания ClickHouse & Vector в подготовленном Docker окружении

## pre-requirement
- Установленный Docker
- Python версии не ниже 3.9
- Ansible версии не ниже 2.10
### Check your stack
В Docker необходимо запустить два контейнера с именами совпадающими с `inventory`
```shell
docker run -d --name centos7 pycontribs/centos:7 sleep 6000000
docker run -d --name ubuntu pycontribs/ubuntu:latest sleep 6000000
```
Проверить наличие и версию ansible можно при помощи команды:
```shell
ansible-playbook --version
```
В качестве параметров Ansible принимает файлы `inventory/prod.yml` и `site.yml`
Запуск плейбука осуществляется следующим образом:
```shell
ansible-playbook -i inventory/prod.yml site.yml
```
## Usage
### Inventory

- Группа "clickhouse" состоит из `1` Docker контейнера `centos`
- Группа "vector" состоит из `1` Docker контейнера `ubuntu`

### group_vars
Состоит ииз двух наборов переменных.

| Переменная                   | Назначение                                                        |
|:-----------------------------|:------------------------------------------------------------------|
| **1**                        |                                                                   |
| `clickhouse_version`         | версия `Clickhouse`                                               |
| `main_package_path.path`     | основной URL адрес для скачивания пакетов `Clickhouse`            |
| `rescue_package_path.path`   | URL адрес пакетов `Clickhouse`, используется при сбое таски       |
| `clickhouse_packages_noarch` | пакеты для установки `Clickhouse`, без зависимости от архитектуры |
| `clickhouse_packages`        | `RPM` пакеты для установки `Clickhouse`                           |
| **2**                        | -                                                                 |
| `vector_version`             | версия `Vector`                                                   |
| `vector_distro.path`         | URL адрес для скачивания пакетов `Vector`                         |
| `vector_distro.package`      | имя установочного пакета `Vector`                                 |
| `vector_dir`                 | каталог для `Vector`                                              |

### Playbook
Cостоит из `2` play
- `Install Clickhouse` - содержит handler и tasks, необходимые для установки `Clickhouse`
- `Install Vector` - содержит tasks, необходимые для установки `Vector`

```shell
- name: Install Clickhouse # начало play с установкой Clickhouse
  hosts: clickhouse # условие установки на хост(ы) из inventory
  debugger: never # отладка
  handlers: # Тут записываются действия, выполнять которые требуется, если какая либо задача произвела изменение и сообщила об этом (notify)
    - name: Start clickhouse service # Здесь выполняется перезагрузка установленного Clickhouse 
      become: true
      ansible.builtin.service:
        name: clickhouse-server
        state: restarted
      tags: clickhouse # <<<<тег, позволяющий ansible выполнять только помеченные тегом задачи
  tasks: # В этом разделе записываются основные задачи для play "Install Clickhouse" 
     - block: # Этот модуль объединяет две задачи (группы подзадач), если первая завершится с ошибкой, запустится вторая - rescue
```