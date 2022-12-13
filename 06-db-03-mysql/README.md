 # Домашнее задание к занятию "6.3. MySQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/blob/virt-11/additional/README.md).

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

В следующих заданиях мы будем продолжать работу с данным контейнером.

### Ответ
[docker-compose.yaml](vm/ansible/stack/docker-compose.yaml)

> В каталоге [vm](vm) реализован следующий вариант:
> - поднимаем виртуалку на bento/centos-7
> - деплоим туда docker+compose
> - на поднятой подсистеме уже играем в MySQL + adminer согласно ТЗ<br>


- Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

- Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-03-mysql/test_data) и 
восстановитесь из него.

```shell
[vagrant@server01 stack]$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                                  NAMES
fa5eeb387327   adminer   "entrypoint.sh docke…"   12 seconds ago   Up 10 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp              stack_adminer_1
13b896a5dd4c   mysql:8   "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   stack_mysql_1
[vagrant@server01 stack]$ sudo docker exec -it 13b896a5dd4c bash
bash-4.4# mysql -u root -p test_db < /data/backup/mysql/test_dump.sql 
Enter password: 
```

- Перейдите в управляющую консоль `mysql` внутри контейнера.
- Используя команду `\h` получите список управляющих команд.
- Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.
```shell
bash-4.4# mysql -u root -p
Enter password: 
mysql> \s
--------------
mysql  Ver 8.0.31 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:		13
Current database:	
Current user:		root@localhost
SSL:			Not in use
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		8.0.31 MySQL Community Server - GPL
Protocol version:	10
Connection:		Localhost via UNIX socket
Server characterset:	utf8mb4
Db     characterset:	utf8mb4
Client characterset:	latin1
Conn.  characterset:	latin1
UNIX socket:		/var/run/mysqld/mysqld.sock
Binary data as:		Hexadecimal
Uptime:			26 min 44 sec

Threads: 2  Questions: 134  Slow queries: 0  Opens: 367  Flush tables: 3  Open tables: 285  Queries per second avg: 0.083
--------------
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test_db            |
+--------------------+
5 rows in set (0.01 sec)
```
- Подключитесь к восстановленной БД и получите список таблиц из этой БД.
- **Приведите в ответе** количество записей с `price` > 300.
```shell
mysql> \u test_db
Database changed
# формирование синтаксиса сначала было проверено в adminer :)
mysql> SELECT * FROM `orders` WHERE `price` > '300';
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0.00 sec)
# ну а тут уже не было, ковычки имеют значение, исправлено до рабочего..
mysql> SELECT COUNT(*) FROM `orders` WHERE `price` > '300';
+----------+
| COUNT(*) |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

### Ответ
- Часть 1, про "создайте"
```shell
mysql> 
CREATE USER 'test'@'localhost' IDENTIFIED BY 'test-pass';
Query OK, 0 rows affected (0.05 sec)

mysql> 
ALTER USER 'test'@'localhost' 
WITH MAX_QUERIES_PER_HOUR 100
PASSWORD EXPIRE INTERVAL 180 DAY
FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 2;
Query OK, 0 rows affected (0.02 sec)

mysql>
ALTER USER 'test'@'localhost' ATTRIBUTE '{"f-name":"James", "l-name":"Pretty"}';
Query OK, 0 rows affected (0.02 sec)
```
- Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
- Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test`
```shell
mysql> GRANT SELECT ON test_db.* TO 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0.02 sec)
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.02 sec)
mysql> select * from information_schema.user_attributes;
+------------------+-----------+-----------------------------------------+
| USER             | HOST      | ATTRIBUTE                               |
+------------------+-----------+-----------------------------------------+
| root             | %         | NULL                                    |
| mysql.infoschema | localhost | NULL                                    |
| mysql.session    | localhost | NULL                                    |
| mysql.sys        | localhost | NULL                                    |
| root             | localhost | NULL                                    |
| test             | localhost | {"f-name": "James", "l-name": "Pretty"} |
+------------------+-----------+-----------------------------------------+
6 rows in set (0.00 sec)
```

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`

### Ответ
Установите профилирование `SET profiling = 1`.
```shell
mysql> use test_db
Database changed
mysql>  SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

Изучите вывод профилирования команд `SHOW PROFILES;`.
```shell
mysql> SHOW PROFILES;
+----------+------------+-------------------+
| Query_ID | Duration   | Query             |
+----------+------------+-------------------+
|        1 | 0.00044950 | SELECT DATABASE() |
|        2 | 0.00213200 | show databases    |
|        3 | 0.00318375 | show tables       |
+----------+------------+-------------------+
3 rows in set, 1 warning (0.00 sec)
```

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.
```shell
mysql> show table status;
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
| Name   | Engine | Version | Row_format | Rows | Avg_row_length | Data_length | Max_data_length | Index_length | Data_free | Auto_increment | Create_time         | Update_time         | Check_time | Collation          | Checksum | Create_options | Comment |
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
| orders | InnoDB |      10 | Dynamic    |    5 |           3276 |       16384 |               0 |            0 |         0 |              6 | 2022-12-13 18:02:49 | 2022-12-13 18:02:49 | NULL       | utf8mb4_0900_ai_ci |     NULL |                |         |
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
1 row in set (0.01 sec)
```

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
```shell
mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0.14 sec)
Records: 5  Duplicates: 0  Warnings: 0
```
- на `InnoDB`
```shell
mysql> ALTER TABLE orders ENGINE = InnoDB;
Query OK, 5 rows affected (0.25 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

```shell
mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------+
| Query_ID | Duration   | Query                                               |
+----------+------------+-----------------------------------------------------+
|        1 | 0.00014800 | SELECT DATABASE()                                   |
|        2 | 0.00044950 | SELECT DATABASE()                                   |
|        3 | 0.00213200 | show databases                                      |
|        4 | 0.00318375 | show tables                                         |
|        5 | 0.00853150 | show table status                                   |
|        6 | 0.18098675 | ALTER TABLE orders ENGINE = MyISAM                  |
|        7 | 0.25250200 | ALTER TABLE orders ENGINE = InnoDB                  |
|        8 | 0.00034200 | SELECT * FROM `orders` WHERE `price` > '300'        |
|        9 | 0.00133625 | SELECT * FROM `orders` WHERE `price` < '300'        |
|       10 | 0.00104100 | SELECT COUNT(*) FROM `orders` WHERE `price` = '300' |
|       11 | 0.13748625 | ALTER TABLE orders ENGINE = MyISAM                  |
|       12 | 0.00055075 | SELECT * FROM `orders` WHERE `price` > '300'        |
|       13 | 0.00156500 | SELECT * FROM `orders` WHERE `price` < '300'        |
|       14 | 0.00090550 | SELECT COUNT(*) FROM `orders` WHERE `price` = '300' |
|       15 | 0.25434875 | ALTER TABLE orders ENGINE = InnoDB                  |
+----------+------------+-----------------------------------------------------+
15 rows in set, 1 warning (0.00 sec)
```

## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
