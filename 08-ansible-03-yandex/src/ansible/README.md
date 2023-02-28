# Описание плейбука site.yml

Предназначен для базового развёртывания ClickHouse & Vector & Lighthouse

## pre-requirement
- [ не обязательно ] Vagrant & Virtualbox 6.1 
- Python версии не ниже 3.9
- Ansible версии не ниже 2.10
### Check your stack
Запуск тестового окружения virtualbox необходимо запускать при помощи Vagrant
```shell
### При первом запуске произойдет закачка дисрибутивов Centos 7 и Ubuntu 18.04
vagrant up
```
Проверить наличие и версию ansible можно при помощи команды:
```shell
ansible-playbook --version
```
В качестве параметров Ansible принимает файлы `inventory/prod.yml` или `inventory/test.yml` и `site.yml` \
Запуск плейбука осуществляется следующим образом:
```shell
ansible-playbook -i inventory/test.yml site.yml
```
## Usage
### Inventory

- Группа "clickhouse" состоит из `1` инстанса `centos`
- Группа "vector" состоит из `1` инстанса `ubuntu`
- Группа "lighthouse" состоит из `1` инстанса `ubuntu`

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
| **2**                        |                                                                   |
| `vector_version`             | версия `Vector`                                                   |
| `vector_distro.path`         | URL адрес для скачивания пакетов `Vector`                         |
| `vector_distro.package`      | имя установочного пакета `Vector`                                 |
| `vector_dir`                 | каталог для установки `Vector`                                    |

### Playbook
Cостоит из `2` play
- `Install Clickhouse` - содержит handler и tasks, необходимые для установки `Clickhouse`
- `Install Vector` - содержит tasks, необходимые для установки `Vector`

```shell
- name: Install Clickhouse # начало play с установкой Clickhouse
  hosts: clickhouse # условие установки на хост(ы) из inventory
  debugger: never # отладка
  handlers: # Тут записываются действия, выполнять которые требуется, если какая либо задача произвела изменение и сообщила об этом (notify)
    - name: Start clickhouse service # <<1>> Здесь выполняется перезагрузка установленного Clickhouse 
      become: true
      ansible.builtin.service:
        name: clickhouse-server
        state: restarted
      tags: clickhouse # <<<<тег, позволяющий ansible выполнять только помеченные тегом задачи
  tasks: # В этом разделе записываются основные задачи для play "Install Clickhouse" 
     - block: # Этот модуль объединяет две задачи (группы подзадач), если первая завершится с ошибкой, запустится вторая - rescue
     # Первый блок отвечает за скачивание дистрибутива
     # Второй блок вызывает установку пакетов задействуя модуль yum
     notify: Start clickhouse service # <<1>> тот самый notify модуля, с именем handler'а, который надо дёрнуть, если были изменения
     # Третий блок рестартит сервис
     # Четвёртый блок отвечает за создание БД Clickhouse
```
```shell
- name: Install Vector # начало play с установкой Vector
  hosts: vector # условие установки на хост(ы) из inventory
  tasks:
    - name: Create directrory for vector "{{ vector_dir }}" # Создание каталога для установки в него Vector
       tags: vector # тег, позволяющий ansible выполнять только помеченные тегом задачи
    - name: Download Vector # Задача на скачивагие дистрибутива
    - name: Extract vector in the installation directory # Распаковка дистрибутива в каталог установки
```
#### Tags
```shell
ansible-playbook -i inventory/prod.yml site.yml --tags XYX
```
| tag                 | Описание                                                                      |
|:--------------------|:------------------------------------------------------------------------------|
| `--tags clickhouse` | будут выполнены все задачи, относящиеся к Clichouse, если добавить к команде  |
| `--tags vector`     | будут выполнены все задачи, относящиеся к Vector                              |
 