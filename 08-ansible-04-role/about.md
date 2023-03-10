# Playbook `site.yml`

Предназначен для базового развёртывания ClickHouse & Vector & Lighthouse

### pre-requirement
- [ не обязательно ] Vagrant & Virtualbox 6.1 
  - Python версии не ниже 3.9
  - Ansible версии не ниже 2.10 
    - Проверить наличие и версию ansible можно при помощи команды:
    `ansible-playbook --version`

### Запуск
Состоит из двух частей:
 - подготовка окружения
 - запуск playbook`a
#### Локальное окружение (inventory/prod.yml)
Необходим установленный virtualbox 6 версии (на 7 возможны проблемы с `vagrant` провайдером)
```shell
### При первом запуске произойдет закачка дистрибутивов Centos 7 и Ubuntu 18.04
### vpn, proxy.. сервера расположенные вне блокировок - в помощь
vagrant up
```
#### Yandex Cloud (inventory/yc.yml)
- Для более сложных сценариев рекомендую создать и использовать для ВМ `сервисный аккаунт` 
- Для работы с `ansible` и последующего доступа в ВМ по протоколу ssh необходимо подготовить RSA ключ
- `Compute Cloud` > `Виртуальные машины` > "Создать ВМ"
- создать две виртуальные машины на `Ubuntu` и одну на `Centos-7`

#### Ansible-playbook
В качестве параметров `Ansible` принимает файлы `inventory/prod.yml` или `inventory/yc.yml` и `site.yml` \
- Запуск плейбука осуществляется следующим образом:
```shell
ansible-playbook -i inventory/prod.yml site.yml
```
- после корректной отработки `playbook`, получим строку вида: \
  - **URL** `http://адрес-Lighthouse/#http://адрес-clickhouse:8123/?user=пользователь`
  - где пользователя и пароль мы задаем в переменных `group_vars` [**All**](./group_vars/all/vars.yml)
  - логи увидим из `Vector`


### Описание
в самом Playbook [site.yml](./site.yml) присутствуют дополнительные пояснительные комментарии
#### Inventory

- Группа "clickhouse" состоит из `1` инстанса `centos`
- Группа "vector" состоит из `1` инстанса `ubuntu`
- Группа "lighthouse" состоит из `1` инстанса `ubuntu`

#### Playbook
Cостоит из `3` ролей и tasks для установки `nginx`
- `Install Clickhouse` - содержит handler и tasks, необходимые для установки `Clickhouse`
- `Install Vector` - содержит handler и tasks, необходимые для установки `Vector`
- `Install Lighthouse` - содержит handler и tasks необходимые для установки `Nginx` и оболочки `Lighthouse` 
