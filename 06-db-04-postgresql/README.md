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
Часть 1\
поднимите, подключитесь:\
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
Часть 2 <br>
**Найдите и приведите** управляющие команды для:
- вывода списка БД - `\l` или `\l+`
- подключения к БД - `\с`
- вывода списка таблиц - `\dt` или `\dt+` (S параметр для системных объектов )
- вывода описания содержимого таблиц -`\d` или `\d+`
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

### Ответ

```shell
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
[vagrant@server64 stack]$ sudo docker exec -it stack_postgres_1 bash
root@1c49f20100a7:/# psql -U postgres test_database < /data/backup/postgres/test_dump.sql 

test_database=# \d+
                                   List of relations
 Schema |     Name      |   Type   |  Owner   | Persistence |    Size    | Description 
--------+---------------+----------+----------+-------------+------------+-------------
 public | orders        | table    | postgres | permanent   | 8192 bytes | 
 public | orders_id_seq | sequence | postgres | permanent   | 8192 bytes | 
(2 rows)

test_database=# ANALYZE;
ANALYZE
test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```
```sql
SELECT
    -- attname from pg_stats - этого достаточно, как пример запроса, но хочется лучше
    tablename, attname, avg_width from pg_stats 
where 
    tablename = 'orders' 
and avg_width in (select max(avg_width) from pg_stats where tablename = 'orders');

 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | title   |        16
(1 row)
```

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).



Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

### Ответ
- Предложите SQL-транзакцию для проведения данной операции.

Интересный кусок, тот что с `COPY`. При шардировании данные перенесены не будут. Надо будет это сделать отдельно.
> https://www.postgresql.org/docs/13/sql-copy.html <br>
> COPY FROM will invoke any triggers and check constraints on the destination table. However, it will not invoke rules.

```sql
begin;
    -- Переименование "старой" orders
  alter table orders rename to orders_old;
    -- Создаём новую orders с шардированием, 
  create table orders (
      like orders_old
      including defaults
      including constraints
      including indexes
  );
  
    -- Создаем две таблицы, наследуемся от orders, вешаем ограничения на price
    -- Партиция orders_1 с  price>499
  create table orders_1 (
      check ( price > 499 )
  ) inherits (orders);
  alter table orders_1 owner to postgres;
  
    -- Партиция orders_2 с price<=499
  create table orders_2 (
     check ( price <= 499 )
  ) inherits (orders);
  alter table orders_2 owner to postgres;

    -- Добавляем индексы на price
  create index orders_1_price ON orders_1 (price);
  create index orders_2_price ON orders_2 (price);

    -- Правило > для сортировки по ключу price
  create rule ins_over_price as
  on insert to orders where 
    (price>499)
  do instead
    insert into orders_1 values(NEW.*);

    -- Правило <= для сортировки по ключу price
  create rule ins_lower_price as
  on insert to orders where 
    (price<=499)
  do instead
    insert into orders_2 values(NEW.*);
    
    -- Копируем данные из "старых" заказов
  insert into orders
  select * from orders_old;
  
    -- Упс1. перепривязка последовательности
  alter table orders_old alter id drop default;
  alter sequence public.orders_id_seq OWNED BY public.orders.id;
end;
```
```shell
# Было
test_database=# \d
              List of relations
 Schema |     Name      |   Type   |  Owner   
--------+---------------+----------+----------
 public | orders        | table    | postgres
 public | orders_id_seq | sequence | postgres
(2 rows)

# Cтало
test_database=# \d+
                                   List of relations
 Schema |     Name      |   Type   |  Owner   | Persistence |    Size    | Description 
--------+---------------+----------+----------+-------------+------------+-------------
 public | orders        | table    | postgres | permanent   | 0 bytes    | 
 public | orders_1      | table    | postgres | permanent   | 8192 bytes | 
 public | orders_2      | table    | postgres | permanent   | 8192 bytes | 
 public | orders_id_seq | sequence | postgres | permanent   | 8192 bytes | 
 public | orders_old    | table    | postgres | permanent   | 8192 bytes | 
(5 rows)
# Упс1 - последовательность - красоты ради стоит перепривязать

test_database=# TABLE orders_1;
 id |       title        | price 
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)

test_database=# TABLE orders_2;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)

test_database=# TABLE orders;
 id |        title         | price 
----+----------------------+-------
  2 | My little database   |   500
  6 | WAL never lies       |   900
  8 | Dbiezdmin            |   501
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(8 rows)

test_database=# 
```

- Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?\
Можно. При создании таблицы и шардировать и навесить правила сразу, всё что выше описано по сути...\
Данные из бэкапа из-за метода copy не попадут в партиции (тк правила не отработают).. о чем выше и в доках.

## Задача 4

- Используя утилиту `pg_dump` создайте бекап БД `test_database`.

- Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?


### Ответ

- Используя утилиту `pg_dump` создайте бекап БД `test_database`.\
```shell
#Бэкапов обычно больше одного, значит стоит сразу облегчить себе жизнь:
root@1c49f20100a7:/# pg_dump -U postgres test_database -v -f /data/backup/postgres/test_database_$(date +"%Y%m%d-%H%M").sql
[vagrant@server64 backup]$ ll
итого 12
-rw-r--r--. 1 root root 2493 дек 16 21:49 test_database_20221216-1849.sql
-rw-r--r--. 1 root root 2493 дек 16 21:50 test_database_20221216-1850.sql
```
- Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

Для начала ~~покурить~~ почитать доки:

https://www.postgresql.org/docs/13/sql-createindex.html <br>
https://www.postgresql.org/docs/13/ddl-constraints.html

**Выводы:**
>`сonstraints` (ограничения) - они для обеспечения целостности данных<br>
>`index` (индексы) — скорость доступа к данным.<br>
> Это две абсолютно не связанные сущности. Первое — часть SQL стандарта, второе нет (тк ни как не связанно с функциональностью языка)<br>
> Разработчик сам решает, в каких случаях применить эти механизмы и использование одного вовсе не требует использование другого.<br>
> `unique` (уникальности) - при добавлении ограничения уникальности (unique constraint) PostgreSQL сам навешивает на указанное поле индекс.

**Итого:**\
Из выше сказанного следует что, можно сделать индекс или ключ для столбика, или ввести ограничение уникальности данных.
```sql
CREATE INDEX ON orders_simple ((lower(title)));
```
update - пока изучал вопросы по шардированию, выяснил что индекс для `orders` работать перестанет тк табличка `partitioned`
```shell
test_database=# \d+ orders
                                                       Table "public.orders"
 Column |         Type          | Collation | Nullable |              Default               | Storage  | Stats target | Description 
--------+-----------------------+-----------+----------+------------------------------------+----------+--------------+-------------
 id     | integer               |           | not null | nextval('orders_id_seq'::regclass) | plain    |              | 
 title  | character varying(80) |           | not null |                                    | extended |              | 
 price  | integer               |           |          | 0                                  | plain    |              | 
Indexes:
    "orders_pkey1" PRIMARY KEY, btree (id)
Rules:
    ins_lower_price AS
    ON INSERT TO orders
   WHERE new.price <= 499 DO INSTEAD  INSERT INTO orders_2 (id, title, price)
  VALUES (new.id, new.title, new.price)
    ins_over_price AS
    ON INSERT TO orders
   WHERE new.price > 499 DO INSTEAD  INSERT INTO orders_1 (id, title, price)
  VALUES (new.id, new.title, new.price)
Child tables: orders_1,
              orders_2
Access method: heap

test_database=# 
```

```sql
-- просто unique
ALTER TABLE public.orders ADD UNIQUE (title);
-- добавим ограничение
ALTER TABLE public.orders ADD CONSTRAINT title_unique UNIQUE (title);
```