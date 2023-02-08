# Домашнее задание к занятию "2. Работа с Playbook"

## Подготовка к выполнению

1. (Необязательно) Изучите, что такое [clickhouse](https://www.youtube.com/watch?v=fjTNS2zkeBs) и [vector](https://www.youtube.com/watch?v=CgEhyffisLY)
2. Создайте свой собственный (или используйте старый) публичный репозиторий на github с произвольным именем.
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
4. Подготовьте хосты в соответствии с группами из предподготовленного playbook.

## Основная часть

1. Приготовьте свой собственный inventory файл `prod.yml`.
2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает [vector](https://vector.dev).
3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.
4. Tasks должны: скачать нужной версии дистрибутив, выполнить распаковку в выбранную директорию, установить vector.
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-02-playbook` на фиксирующий коммит, в ответ предоставьте ссылку на него.

---
### Ответ

0. Подготовка стека:
   - Vagrant > Ubuntu > Ansible + lint \ Docker + Compose
   - ```shell
     # копируем плейбуку внутрь
     vagrant scp ../ansible/stack/playbook server82.lab:/opt/stack
     # запускаем Centos7, тк в плейбуке rpm
     root@server82:/opt/stack/playbook# docker run -d --name centos7 pycontribs/centos:7 sleep 6000000
     29b1d50456e6cf323a5cebdb937b6bc163a30248aa754b7dce5d1de438d7e9dd
     root@server82:/opt/stack/playbook# docker ps
     CONTAINER ID   IMAGE                 COMMAND           CREATED         STATUS         PORTS     NAMES
     29b1d50456e6   pycontribs/centos:7   "sleep 6000000"   5 seconds ago   Up 4 seconds             centos7
      ```
1. Приготовьте свой собственный inventory файл `prod.yml`. [prod.yml](src%2Fansible%2Fstack%2Fplaybook%2Finventory%2Fprod.yml)
2. Допишите playbook: 
   - Для начала разбираемся с `Clickhouse`
     - в репо [Clickhouse](https://packages.clickhouse.com/rpm/stable/) нет файлов из плейбуки, на репо яндекса тоже нет.
     + переделал логику - сейчас используются два репозитория, пакеты тоже скачиваются успешно
     + исправлен старт и рестарт субд - на стоковой плейбуке крашилось
     + Запуск `ansible-lint`
     ```shell
     root@server82:/opt/stack/playbook# ansible-lint site.yml
     WARNING: PATH altered to include /usr/bin
     WARNING  Overriding detected file kind 'yaml' with 'playbook' for given positional argument: site.yml
     ```
     Ошибки были с переменными, сейчас - нет. \
     Первое предупреждение появляется из-за установки `ansible` через `pip3` в дир. пользователя, a `python` живет как надо. \
     Второе предупреждение решилось `cp site.yml playbook.yml` для проведения повторного запуска.

   - Vector - added
3. Логи выполнения всякого
 <details><summary>Clickhouse</summary>

```shell
root@server82:/opt/stack/playbook# ansible-playbook -i inventory/prod.yml site.yml --check

PLAY [Install Clickhouse] ******************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************
ok: [centos7]

TASK [Get clickhouse distrib noarch Get clickhouse distrib noarch  from https://packages.clickhouse.com/rpm/stable/] ***********************************************
ok: [centos7] => (item=clickhouse-client)
ok: [centos7] => (item=clickhouse-server)

TASK [Get clickhouse distrib from https://packages.clickhouse.com/rpm/stable/] *************************************************************************************
ok: [centos7] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] *********************************************************************************************************************************
ok: [centos7]

TASK [Start clickhouse service] ************************************************************************************************************************************
changed: [centos7]

TASK [Create database] *********************************************************************************************************************************************
skipping: [centos7]

PLAY RECAP *********************************************************************************************************************************************************
centos7                    : ok=5    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```

```shell
root@server82:/opt/stack/playbook# ansible-playbook -i inventory/prod.yml site.yml --diff

PLAY [Install Clickhouse] ******************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************
ok: [centos7]

TASK [Get clickhouse distrib noarch Get clickhouse distrib noarch  from https://packages.clickhouse.com/rpm/stable/] ***********************************************
ok: [centos7] => (item=clickhouse-client)
ok: [centos7] => (item=clickhouse-server)

TASK [Get clickhouse distrib from https://packages.clickhouse.com/rpm/stable/] *************************************************************************************
ok: [centos7] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] *********************************************************************************************************************************
ok: [centos7]

TASK [Start clickhouse service] ************************************************************************************************************************************
changed: [centos7]

TASK [Create database] *********************************************************************************************************************************************
ok: [centos7]

PLAY RECAP *********************************************************************************************************************************************************
centos7                    : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

```shell
root@server82:/opt/stack/playbook# ansible-playbook -i inventory/prod.yml site.yml

PLAY [Install Clickhouse] ******************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************
ok: [centos7]

TASK [Get clickhouse distrib noarch Get clickhouse distrib noarch  from https://packages.clickhouse.com/rpm/stable/] ***********************************************
changed: [centos7] => (item=clickhouse-client)
changed: [centos7] => (item=clickhouse-server)

TASK [Get clickhouse distrib from https://packages.clickhouse.com/rpm/stable/] *************************************************************************************
changed: [centos7] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] *********************************************************************************************************************************
changed: [centos7]

TASK [Start clickhouse service] ************************************************************************************************************************************
changed: [centos7]

TASK [Create database] *********************************************************************************************************************************************
changed: [centos7]

RUNNING HANDLER [Start clickhouse service] *************************************************************************************************************************
changed: [centos7]

PLAY RECAP *********************************************************************************************************************************************************
centos7                    : ok=7    changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
</details>
<details><summary>Vector</summary>

```shell
vagrant@server82:/opt/stack/playbook$ ansible-playbook -i inventory/prod.yml site.yml

PLAY [Install Clickhouse] ******************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************
ok: [centos7]

TASK [Get clickhouse distrib noarch Get clickhouse distrib noarch  from https://packages.clickhouse.com/rpm/stable/] ***********************************************
ok: [centos7] => (item=clickhouse-client)
ok: [centos7] => (item=clickhouse-server)

TASK [Get clickhouse distrib from https://packages.clickhouse.com/rpm/stable/] *************************************************************************************
ok: [centos7] => (item=clickhouse-common-static)

TASK [Install clickhouse packages] *********************************************************************************************************************************
ok: [centos7]

TASK [Start clickhouse service] ************************************************************************************************************************************
ok: [centos7]

TASK [Create database] *********************************************************************************************************************************************
ok: [centos7]

PLAY [Install Vector] **********************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************
ok: [ubuntu]

TASK [Create directrory for vector "/opt/vector"] ******************************************************************************************************************
ok: [ubuntu]

TASK [Download Vector] *********************************************************************************************************************************************
ok: [ubuntu]

TASK [Extract vector in the installation directory] ****************************************************************************************************************
ok: [ubuntu]

PLAY RECAP *********************************************************************************************************************************************************
centos7                    : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
</details>

4. Подготовьте README.md файл по своему playbook. <br>
В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
   - [README.md](src%2Fansible%2Fstack%2Fplaybook%2FREADME.md) - Описание
   - [site.yml](src%2Fansible%2Fstack%2Fplaybook%2Fsite.yml) - Playbook
   - [src](src) - Рабочая директория со всеми материалами по домашнему заданию