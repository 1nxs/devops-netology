# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ
Часть 1, поднимите, подключитесь\
[docker-compose.yaml](vm/ansible/stack/docker-compose.yaml)
<details>
В каталоге [vm](vm) реализован следующий вариант:
- поднимаем виртуалку на bento/centos-7
- деплоим туда docker+compose
- на поднятой подсистеме уже играем в PostgreSQL + pgadmin согласно ТЗ<br>
</details>

```shell
❯ vagrant ssh
Last login: Fri Dec 16 17:44:38 2022 from 10.0.2.2
[vagrant@server64 ~]$ sudo docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                       NAMES
1c49f20100a7   postgres:13   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   stack_postgres_1
cd9b803f5f1e   adminer       "entrypoint.sh php -…"   2 minutes ago   Up 2 minutes   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   stack_adminer_1
[vagrant@server64 ~]$ sudo docker exec -it stack_postgres_1 psql --username postgres
psql (13.9 (Debian 13.9-1.pgdg110+1))
Type "help" for help.
postgres=# 
```
Часть 2\
**Найдите и приведите** управляющие команды для:
- вывода списка БД - `\l` или `\l+`
- подключения к БД - `\с`
- вывода списка таблиц - `\dt` или `\dt+` (S параметр для системных объектов )
- вывода описания содержимого таблиц -`\d`
- выхода из psql - `\q` 

**CLI под катом:**
<details>

```shell
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
postgres=# \c postgres 
You are now connected to database "postgres" as user "postgres".
postgres=# \dt
Did not find any relations.
postgres=# \dt+
Did not find any relations.
postgres=# \dtS
                    List of relations
   Schema   |          Name           | Type  |  Owner   
------------+-------------------------+-------+----------
 pg_catalog | pg_aggregate            | table | postgres
 pg_catalog | pg_am                   | table | postgres
---
 pg_catalog | pg_user_mapping         | table | postgres
(62 rows)
postgres=# \dtS pg_type 
            List of relations
   Schema   |  Name   | Type  |  Owner   
------------+---------+-------+----------
 pg_catalog | pg_type | table | postgres
(1 row)
postgres=# \dtS+ pg_type 
                              List of relations
   Schema   |  Name   | Type  |  Owner   | Persistence |  Size  | Description 
------------+---------+-------+----------+-------------+--------+-------------
 pg_catalog | pg_type | table | postgres | permanent   | 120 kB | 
(1 row)
\d pg_database
               Table "pg_catalog.pg_database"
    Column     |   Type    | Collation | Nullable | Default 
---------------+-----------+-----------+----------+---------
 oid           | oid       |           | not null | 
 datname       | name      |           | not null | 
 datdba        | oid       |           | not null | 
 encoding      | integer   |           | not null | 
 datcollate    | name      |           | not null | 
 datctype      | name      |           | not null | 
 datistemplate | boolean   |           | not null | 
 datallowconn  | boolean   |           | not null | 
 datconnlimit  | integer   |           | not null | 
 datlastsysoid | oid       |           | not null | 
 datfrozenxid  | xid       |           | not null | 
 datminmxid    | xid       |           | not null | 
 dattablespace | oid       |           | not null | 
 datacl        | aclitem[] |           |          | 
Indexes:
    "pg_database_datname_index" UNIQUE, btree (datname), tablespace "pg_global"
    "pg_database_oid_index" UNIQUE, btree (oid), tablespace "pg_global"
Tablespace: "pg_global"

postgres=# \q
[vagrant@server64 ~]$ 
```
</details>
## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
