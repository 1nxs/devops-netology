# Домашнее задание к занятию "4. Работа с roles"

## Подготовка к выполнению
1. (Необязательно) Познакомтесь с [lighthouse](https://youtu.be/ymlrNlaHzIY?t=929)
2. Создайте два пустых публичных репозитория в любом своём проекте: vector-role и lighthouse-role.
3. Добавьте публичную часть своего ключа к своему профилю в github.

## Основная часть

Наша основная цель - разбить наш playbook на отдельные roles. Задача: сделать roles для clickhouse, vector и lighthouse и написать playbook для использования этих ролей. Ожидаемый результат: существуют три ваших репозитория: два с roles и один с playbook.

1. Создать в старой версии playbook файл `requirements.yml` и заполнить его следующим содержимым:

   ```yaml
   ---
     - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
       scm: git
       version: "1.11.0"
       name: clickhouse 
   ```


3. Создать новый каталог с ролью при помощи `ansible-galaxy role init vector-role`.
4. На основе tasks из старого playbook заполните новую role. Разнесите переменные между `vars` и `default`. 
5. Перенести нужные шаблоны конфигов в `templates`.
6. Описать в `README.md` обе роли и их параметры.
7. Повторите шаги 3-6 для lighthouse. Помните, что одна роль должна настраивать один продукт.
8. Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию Добавьте roles в `requirements.yml` в playbook.
9. Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения `roles` с `tasks`.
10. Выложите playbook в репозиторий.
11. В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.

---
### Ответ

Блок 1. 
1. Создать в старой версии playbook файл `requirements.yml` и заполнить его следующим содержимым:

   <details><summary>yaml</summary>
   
   ```yaml
   ---
     - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
       scm: git
       version: "1.11.0"
       name: clickhouse 
   ```
</details>

2. При помощи `ansible-galaxy` скачать себе эту роль.

 - В своём файле поменял на текущую версию релиза
 - загрузил роль к себе
```shell
❯ ansible-galaxy install -r requirements.yml -p roles
Starting galaxy role install process
- extracting clickhouse to /home/inxss/pro/devops-netology/08-ansible-04-role/roles/clickhouse
- clickhouse (1.13) was installed successfully
```

Блок 2.
3. Создать новый каталог с ролью при помощи `ansible-galaxy role init vector-role`.
4. На основе tasks из старого playbook заполните новую role. Разнесите переменные между `vars` и `default`. 
5. Перенести нужные шаблоны конфигов в `templates`.
6. Описать в `README.md` обе роли и их параметры.
7. Повторите шаги 3-6 для lighthouse. Помните, что одна роль должна настраивать один продукт.

```shell
❯ ansible-galaxy init clickhouse-role
- Role clickhouse-role was created successfully
❯ ansible-galaxy init vector-role
- Role clickhouse-role was created successfully
❯ ansible-galaxy init vector-role
- Role clickhouse-role was created successfully
```
- настроил путь для ролей - [ansible.cfg](./ansible.cfg)
- подготовил роль Clickhouse
- подготовил роль Vector
- заполнил readme и meta

Блок 3.
8. Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию Добавьте roles в `requirements.yml` в playbook.
9. Переработайте playbook на использование roles. Не забудьте про зависимости lighthouse и возможности совмещения `roles` с `tasks`.
10. Выложите playbook в репозиторий.

- создал репозитории
- проставил tag "1.0.0"
- переработал Playbook, оставив таски (пре\пост) для nginx, остальное убрав в роли
- переработал `requirements.yml` и привёз роли с git
```shell
❯ ansible-galaxy install -r requirements.yml -p roles --force
Starting galaxy role install process
- extracting clickhouse-role to /home/inxss/pro/devops-netology/08-ansible-04-role/roles/clickhouse-role
- clickhouse-role (1.0.0) was installed successfully
- extracting vector-role to /home/inxss/pro/devops-netology/08-ansible-04-role/roles/vector-role
- vector-role (1.0.0) was installed successfully
- extracting lighthouse-role to /home/inxss/pro/devops-netology/08-ansible-04-role/roles/lighthouse-role
- lighthouse-role (1.0.0) was installed successfully
```
