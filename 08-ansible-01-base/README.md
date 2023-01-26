# Домашнее задание к занятию "1. Введение в Ansible"

## Подготовка к выполнению
1. Установите ansible версии 2.10 или выше.
2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.
2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.
2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.
3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.
4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
6. Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

---

### Ответ

#### Самоконтроль выполненения задания

1. Где расположен файл с `some_fact` из второго пункта задания?
   - `./group_vars/all/examp.yml`
2. Какая команда нужна для запуска вашего `playbook` на окружении `test.yml`?
   - `ansible-playbook  -i inventory/test.yml site.yml`
4. Какой командой можно зашифровать файл?
   - `ansible-vault encrypt group_vars/el/examp.yml`
4. Какой командой можно расшифровать файл?
   - `ansible-vault decrypt group_vars/el/examp.yml`
5. Можно ли посмотреть содержимое зашифрованного файла без команды расшифровки файла? Если можно, то как?
   - `ansible-vault view group_vars/deb/examp.yml`
6. Как выглядит команда запуска `playbook`, если переменные зашифрованы?
   - `ansible-playbook  -i playbook/inventory/prod.yml site.yml --ask-vault-pass`
   - `ansible-playbook -i playbook/inventory/prod.yml playbook/site.yml --vault-password-file playbook/strong.pwd`
7. Как называется модуль подключения к host на windows?
   - [winrm](https://docs.ansible.com/ansible/latest/os_guide/windows_winrm.html)
   - [pspr](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/psrp_connection.html)
8. Приведите полный текст команды для поиска информации в документации ansible для модуля подключений ssh
   - `ansible-doc -t connection ssh`
9. Какой параметр из модуля подключения `ssh` необходим для того, чтобы определить пользователя, под которым необходимо совершать подключение?
   - `remote_user`

#### Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.
```shell
vagrant@server81:/opt/stack/playbook$ ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] ****************************************************************

TASK [Gathering Facts] ***************************************************************
ok: [localhost]

TASK [Print OS] **********************************************************************
ok: [localhost] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ********************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP ***************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
```shell
TASK [Print fact] ********************************************************************
ok: [localhost] => {
    "msg": "all default fact"
}
```
3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
```shell
vagrant@server81:/opt/stack/playbook$ sudo docker run -d --name centos7 1nxs/centos:7 sleep 10000000
vagrant@server81:/opt/stack/playbook$ sudo docker run -d --name ubuntu 1nxs/ubuntu sleep 10000000
vagrant@server81:/opt/stack/playbook$ sudo docker ps
CONTAINER ID   IMAGE                 COMMAND            CREATED              STATUS              PORTS     NAMES
c6fe4811883c   1nxs/centos:7   "sleep 10000000"   About a minute ago   Up About a minute             centos7
baa59c3dcca7   1nxs/ubuntu     "sleep 10000000"   18 minutes ago       Up 18 minutes                 ubuntu

```
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
```shell
vagrant@server81:/opt/stack/playbook$ ansible-playbook site.yml -i inventory/prod.yml 

PLAY [Print os facts] ***********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] *****************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ***************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP **********************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
6. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
```shell
vagrant@server81:/opt/stack/playbook$ cat group_vars/{deb,el}/*
---
  some_fact: "deb default fact"
---
  some_fact: "el default fact"

```
7. Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
```shell
vagrant@server81:/opt/stack/playbook$ ansible-playbook site.yml -i inventory/prod.yml 

PLAY [Print os facts] ***********************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] *****************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ***************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP **********************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
```shell
vagrant@server81:/opt/stack/playbook$ ansible-vault encrypt group_vars/deb/*
vagrant@server81:/opt/stack/playbook$ ansible-vault encrypt group_vars/el/*
```
8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
```shell
vagrant@server81:/opt/stack/playbook$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-password
Vault password: 

PLAY [Print os facts] ****************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ********************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ***************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
```shell
vagrant@server81:/opt/stack$ cat playbook/inventory/prod.yml
---
  local:
    hosts:
      localOS:
        ansible_connection: local
```
11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
```shell
vagrant@server81:/opt/stack$ ansible-playbook -i playbook/inventory/prod.yml playbook/site.yml --ask-vault-password
Vault password: 

PLAY [Print os facts] ****************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [localOS]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **********************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localOS] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ********************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [localOS] => {
    "msg": "all default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ***************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localOS                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.
- [playbook](src%2Fansible%2Fstack%2Fplaybook)

---
Использование файла пароля
```shell
# Создаём файл и пишем в него пароль
vagrant@server81:/opt/stack/playbook$ echo 'netology' > strong.pwd 
# Исключаем его из репозитория - пароль же
$ echo 'strong.pwd' >> .gitignore
# Даём права, иначе ошибка 8
chmod a-x strong.pwd

# Исполняем всё то-же самое но уже с файлом
vagrant@server81:/opt/stack$ ansible-playbook -i playbook/inventory/prod.yml playbook/site.yml --vault-password-file playbook/strong.pwd 
```

