# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/blob/virt-11/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

### Ответ
[docker-compose.yaml](vm/ansible/stack/docker-compose.yaml)

В каталоге [vm](vm) реализован следующий вариант:
- поднимаем виртуалку на bento/centos-7
- деплоим туда docker+compose
- на поднятой подсистеме уже играем в PostgreSQL + pgadmin согласно ТЗ<br>

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db
### Ответ
Step 1
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db
```shell
sudo docker exec -it 5979b78de63f psql -U postgres
CREATE USER "test-admin-user" WITH LOGIN;
CREATE DATABASE test_db;
\c test_db 
```
Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Опираясь на доку https://postgrespro.ru/docs/postgresql/12/datatype-numeric <br>
выбран тип `SERIAL` - в основе лежит тип INTEGER, однако значением по умолчанию для величин этого типа является не NULL, а следующее целое число.\
Это удобно для создания столбцов с уникальными идентификаторами.
```sql
CREATE TABLE orders (
	id serial PRIMARY KEY, 
	"наименование" TEXT, 
	"цена" INT
);
```

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, **index**)
- заказ (foreign key orders)

```sql
CREATE TABLE clients (
	id serial PRIMARY KEY, 
	"фамилия" TEXT, 
	"cтрана проживания" TEXT, 
	"заказ" INT REFERENCES orders (id)
);
```
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db
```sql
GRANT ALL ON TABLE clients, orders TO "test-admin-user";
CREATE USER "test-simple-user" WITH LOGIN;
GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE clients,orders TO "test-simple-user";
```

Приведите:
- итоговый список БД после выполнения пунктов выше,
```shell
test_db=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)
```
- описание таблиц (describe)
```shell
test_db=# \d+ orders
                                                   Table "public.orders"
    Column    |  Type   | Collation | Nullable |              Default               | Storage  | Stats target | Description 
--------------+---------+-----------+----------+------------------------------------+----------+--------------+-------------
 id           | integer |           | not null | nextval('orders_id_seq'::regclass) | plain    |              | 
 наименование | text    |           |          |                                    | extended |              | 
 цена         | integer |           |          |                                    | plain    |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap
test_db=# 
```
```shell
test_db=# \d+ clients
                                                      Table "public.clients"
      Column       |  Type   | Collation | Nullable |               Default               | Storage  | Stats target | Description 
-------------------+---------+-----------+----------+-------------------------------------+----------+--------------+-------------
 id                | integer |           | not null | nextval('clients_id_seq'::regclass) | plain    |              | 
 фамилия           | text    |           |          |                                     | extended |              | 
 cтрана проживания | text    |           |          |                                     | extended |              | 
 заказ             | integer |           |          |                                     | plain    |              | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap
test_db=# 

```
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
```sql
SELECT table_name, array_agg(privilege_type), grantee
FROM information_schema.table_privileges
WHERE table_name = 'orders' OR table_name = 'clients'
GROUP BY table_name, grantee;
```
```shell
test_db=# 
 table_name |                         array_agg                         |     grantee      
------------+-----------------------------------------------------------+------------------
 clients    | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | postgres
 clients    | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | test-admin-user
 clients    | {DELETE,INSERT,SELECT,UPDATE}                             | test-simple-user
 orders     | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | postgres
 orders     | {INSERT,TRIGGER,REFERENCES,TRUNCATE,DELETE,UPDATE,SELECT} | test-admin-user
 orders     | {DELETE,SELECT,UPDATE,INSERT}                             | test-simple-user
(6 rows)
test_db=# 
```
- список пользователей с правами над таблицами test_db
```shell
test_db=# \du
                                       List of roles
    Role name     |                         Attributes                         | Member of 
------------------+------------------------------------------------------------+-----------
 postgres         | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 test-admin-user  | Superuser, No inheritance                                  | {}
 test-simple-user |                                                            | {}
test_db=#
```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

### Ответ

```sql
INSERT INTO orders ("наименование", "цена" ) VALUES ('Шоколад', '10'), ('Принтер', '3000'), ('Книга', '500'), ('Монитор', '7000'), ('Гитара', '4000');
INSERT INTO clients ("фамилия", "cтрана проживания") VALUES ('Иванов Иван Иванович', 'USA'), ('Петров Петр Петрович', 'Canada'), ('Иоганн Себастьян Бах', 'Japan'), ('Ронни Джеймс Дио', 'Russia'), ('Ritchie Blackmore', 'Russia');
```
про кол-во записей -  можно было бы `select * from XXX` но если записей много то это как-то "криво"\
запросы объединяем через `union all` https://postgrespro.ru/docs/postgresql/12/typeconv-union-case
```sql
SELECT 'clients' AS name_table,  COUNT(*) AS number_rows  FROM clients
union all
SELECT 'orders' AS name_table,  COUNT(*) AS number_rows  FROM orders;

 name_table | number_rows 
------------+-------------
 clients    |           5
 orders     |           5
(2 rows)

```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказка - используйте директиву `UPDATE`.

### Ответ

```sql
update clients set "заказ"=13 where фамилия='Иванов Иван Иванович';
UPDATE clients SET "заказ"=14 WHERE id=2;
UPDATE clients SET "заказ"=15 WHERE id=3;
```
```shell
test_db=# select * from clients where "заказ" is not null;
 id |       фамилия        | cтрана проживания | заказ 
----+----------------------+-------------------+-------
  2 | Петров Петр Петрович | Canada            |    14
  3 | Иоганн Себастьян Бах | Japan             |    15
  1 | Иванов Иван Иванович | USA               |    13
(3 rows)
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

### Ответ
Postgres делает предположения по `запросу` на основе собираемой статистики.
```shell
test_db=# explain select * from clients where "заказ" is not null;
                        QUERY PLAN                         
-----------------------------------------------------------
 Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72)
   Filter: ("заказ" IS NOT NULL)
(2 rows)
```
- Выполняем последовательное чтение в `clients`
- Стоимость вычисляется исходя из примерного вывода строк
  - `0.00` - стоимость, стартовое значение
  - `18.10` - стоимость получения всех строчек
  - `806` - примерное кол-во проверенных строк
  - `72` - средняя длина строки в байтах
- применённый фильтр

> Дополнив запрос параметром `analyze` - будет произведено выполнение запроса, и данные дополнятся уже точными, `actual` значениями:
```shell
test_db=# explain analyze select * from clients where "заказ" is not null;
                                             QUERY PLAN                                              
-----------------------------------------------------------------------------------------------------
 Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72) (actual time=0.023..0.024 rows=3 loops=1)
   Filter: ("заказ" IS NOT NULL)
   Rows Removed by Filter: 2
 Planning Time: 0.049 ms
 Execution Time: 0.050 ms
(5 rows)

```
## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления.

### Ответ

* Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).
* Остановите контейнер с PostgreSQL (но не удаляйте volumes).
```shell
[vagrant@server01 ~]$ sudo docker exec -it 6b84086517ad bash
root@6b84086517ad:/# pg_dump -U postgres -F t test_db > /data/backup/postgres/test_db.tar
[vagrant@server01 stack]$ cd backup/
[vagrant@server01 backup]$ ll
итого 16
-rw-r--r--. 1 root root 14848 дек  4 20:54 test_db.tar
[vagrant@server01 stack]$ sudo docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED        STATUS       PORTS                                       NAMES
39c107c6084a   adminer       "entrypoint.sh docke…"   24 hours ago   Up 4 hours   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   stack_adminer_1
6b84086517ad   postgres:12   "docker-entrypoint.s…"   24 hours ago   Up 4 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   stack_postgres_1
[vagrant@server01 stack]$ sudo docker stop 6b84086517ad
6b84086517ad
[vagrant@server01 stack]$ sudo docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED        STATUS                      PORTS                                       NAMES
39c107c6084a   adminer       "entrypoint.sh docke…"   24 hours ago   Up 4 hours                  0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   stack_adminer_1
6b84086517ad   postgres:12   "docker-entrypoint.s…"   24 hours ago   Exited (0) 59 seconds ago                                               stack_postgres_1
```
* Поднимите новый пустой контейнер с PostgreSQL.
```shell
[vagrant@server01 stack]$ sudo docker rm 6b84086517ad
6b84086517ad
[vagrant@server01 stack]$ sudo docker-compose up -d
stack_adminer_1 is up-to-date
Creating stack_postgres_1 ... done
[vagrant@server01 stack]$ sudo docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
095048d1fad0   postgres:12   "docker-entrypoint.s…"   14 seconds ago   Up 11 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   stack_postgres_1
39c107c6084a   adminer       "entrypoint.sh docke…"   25 hours ago     Up 4 hours      0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   stack_adminer_1
```

Восстановите БД test_db в новом контейнере.

```shell
[vagrant@server01 stack]$ sudo docker exec -it 095048d1fad0 bash
root@095048d1fad0:/# pg_restore -U postgres --verbose -C -d postgres /data/backup/postgres/test_db.tar
[vagrant@server01 stack]$ sudo docker exec -it 095048d1fad0 psql -U postgres
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

postgres=#
postgres=# CREATE USER "test-admin-user" WITH LOGIN;
postgres=# CREATE USER "test-simple-user" WITH LOGIN;
postgres=# \c test_db 

test_db=# explain analyze select * from clients where "заказ" is not null;
                                             QUERY PLAN                                              
-----------------------------------------------------------------------------------------------------
 Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72) (actual time=0.070..0.073 rows=3 loops=1)
   Filter: ("заказ" IS NOT NULL)
   Rows Removed by Filter: 2
 Planning Time: 1.437 ms
 Execution Time: 2.198 ms
(5 rows)
test_db=#
```