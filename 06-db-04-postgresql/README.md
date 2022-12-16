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
Часть 2\
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
Интересный кусок, тот что с `COPY`. При шардировании данные перенесены не будут. Надо будет это сделать отдельно.

https://www.postgresql.org/docs/13/sql-copy.html
> COPY FROM will invoke any triggers and check constraints on the destination table. However, it will not invoke rules.

```postgres-sql
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

-- Партиция orders_2 с price<=499
  create table orders_2 (
     check ( price <= 499 )
  ) inherits (orders);

-- Добавляем индексы на price
  create index orders_1_price ON orders_1 (price);
  create index orders_2_price ON orders_2 (price);

-- Правило > для сортировки по ключу price
  create rule ins_over_price as
  on insert to orders where 
    (price>499)
  do instead
    insert into orders_1 values(NEW.*);



```

<details>

```sql
--
-- PostgreSQL database dump
--

-- Dumped from database version 13.9 (Debian 13.9-1.pgdg110+1)
-- Dumped by pg_dump version 13.9 (Debian 13.9-1.pgdg110+1)

-- Started on 2022-12-16 18:50:24 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16385)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) NOT NULL,
    price integer DEFAULT 0
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16389)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 2994 (class 0 OID 0)
-- Dependencies: 201
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 2854 (class 2604 OID 16391)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 2987 (class 0 OID 16385)
-- Dependencies: 200
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, title, price) FROM stdin;
1       War and peace   100
2       My little database      500
3       Adventure psql time     300
4       Server gravity falls    300
5       Log gossips     123
6       WAL never lies  900
7       Me and my bash-pet      499
8       Dbiezdmin       501
\.


--
-- TOC entry 2995 (class 0 OID 0)
-- Dependencies: 201
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 8, true);


--
-- TOC entry 2856 (class 2606 OID 16393)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


-- Completed on 2022-12-16 18:50:24 UTC

--
-- PostgreSQL database dump complete
--
```

</details>

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

https://www.postgresql.org/docs/13/sql-createindex.html

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
```sql
-- просто unique
ALTER TABLE public.orders ADD UNIQUE (title);
-- добавим ограничение
ALTER TABLE public.orders ADD CONSTRAINT title_unique UNIQUE (title);
```