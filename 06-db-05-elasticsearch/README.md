# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

### Ответ

<details>

* **Очень много** времени ушло на попытку сборки стека
* На версии `8.5.3` - ругается на java, пришлось брать версии младше.
* На версии `8.2.0` спустя 100500 попыток сборки взлетело

- Build
```shell
[vagrant@server65 ~]$ sudo docker login
[vagrant@server65 ~]$ sudo docker build -t 1nxs/elk:0.6 . 
```

- Run

```shell
# вот иначе всё падает ()
[vagrant@server65 stack]$ sudo sysctl -w vm.max_map_count=262144
vm.max_map_count = 262144

[vagrant@server65 ~]$ sudo docker run --rm -d --name elastic -p 9200:9200 -p 9300:9300 1nxs/elk:0.6
[vagrant@server65 ~]$ sudo docker exec -it elastic bash
```
#### Ошибка нехватки памяти
> max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

Вобщем-то понятно, что нужно лечить хост.
1. смотрим, и подтверждаем свои догадки
```shell
[vagrant@server65 stack]$ more /proc/sys/vm/max_map_count
65530
```
2. Берем напильник
```shell
[vagrant@server65 stack]$ sudo sysctl -w vm.max_map_count=262144
[vagrant@server65 stack]$ sudo sysctl -p
```
3. запускаем контейнер

</details>

[Dockerfile](./src/Dockerfile) <br>
ссылка на DockerHub `docker pull 1nxs/elk:0.6` <br> 
https://hub.docker.com/r/1nxs/elk/tags

- После сборки контейнера стоит задать пароли
```shell
[vagrant@server65 ~]$ sudo docker ps
CONTAINER ID   IMAGE          COMMAND               CREATED          STATUS          PORTS                                                                                  NAMES
c5ec5c199b35   1nxs/elk:0.6   "bin/elasticsearch"   28 minutes ago   Up 28 minutes   0.0.0.0:9200->9200/tcp, :::9200->9200/tcp, 0.0.0.0:9300->9300/tcp, :::9300->9300/tcp   elastic
[vagrant@server65 ~]$ sudo docker exec -it elastic bash
# Директива - elasticsearch-setup-passwords interactive для нашей задачи слишком брутальна
[elasticsearch@d480e63dbe74 elasticsearch-8.2.0]$ bin/elasticsearch-reset-password --interactive --username elastic

```

- Далее удастся получить ответ на запрос:
```shell
vagrant@server65 ~]$ curl --insecure -u elastic https://localhost:9200
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "2Eo54a4jToSmsq0B1vNgQg",
  "version" : {
    "number" : "8.2.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "b174af62e8dd9f4ac4d25875e9381ffe2b9282c5",
    "build_date" : "2022-04-20T10:35:10.180408517Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
[vagrant@server65 ~]$
``` 

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ
* Добавьте 3 индекса
```shell
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic "https://localhost:9200/ind-1?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 1,  
      "number_of_replicas": 0 
    }
  }
}
'
Enter host password for user 'elastic':
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
```
```shell
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic "https://localhost:9200/ind-2?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 2,  
      "number_of_replicas": 1 
    }
  }
}
'
Enter host password for user 'elastic':
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
```
```shell
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic "https://localhost:9200/ind-3?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 4,  
      "number_of_replicas": 2 
    }
  }
}
'
Enter host password for user 'elastic':
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
```
* Получите список индексов и их статусов, используя API и приведите в ответе на задание.
* Получите состояние кластера elasticsearch, используя API.
```shell
vagrant@server65 ~]$ curl -X GET --insecure -u elastic "https://localhost:9200/_cat/indices?v=true"
Enter host password for user 'elastic':
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   ind-2 lC2P7WJnQI27Esxl9ItnBw   2   1          0            0       450b           450b
yellow open   ind-3 LLnpGgkzQJOLe8XRHiViMg   4   2          0            0       900b           900b
green  open   ind-1 rcf2AZshRuGNH9vzqb74kw   1   0          0            0       225b           225b

[vagrant@server65 ~]$ curl -X GET --insecure -u elastic "https://localhost:9200/_cluster/health/ind-1?pretty"
Enter host password for user 'elastic':
{
  "cluster_name" : "elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic "https://localhost:9200/_cluster/health/ind-2?pretty"
Enter host password for user 'elastic':
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 2,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 2,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 47.368421052631575
}
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic "https://localhost:9200/_cluster/health/ind-3?pretty"
Enter host password for user 'elastic':
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 8,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 47.368421052631575
}
[vagrant@server65 ~]$ 
```
статус кластера:
```shell
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic "https://localhost:9200/_cluster/health/ind-2?pretty"
Enter host password for user 'elastic':
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 7,
  "active_shards" : 7,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}
```
* Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Оранжевым по чёрному - у нас `"number_of_nodes" : 1` , а индексы у нас с репликацией, ну а делать её выходит некуда.

* Удалите все индексы.
```shell
[vagrant@server65 ~]$ curl -X DELETE --insecure -u elastic "https://localhost:9200/ind-1?pretty"
[vagrant@server65 ~]$ curl -X DELETE --insecure -u elastic "https://localhost:9200/ind-2?pretty"
[vagrant@server65 ~]$ curl -X DELETE --insecure -u elastic "https://localhost:9200/ind-3?pretty"

[2022-12-27T00:11:19,695][INFO ][o.e.c.m.MetadataDeleteIndexService] [netology_test] [ind-1/rcf2AZshRuGNH9vzqb74kw] deleting index
[2022-12-27T00:11:28,011][INFO ][o.e.c.m.MetadataDeleteIndexService] [netology_test] [ind-2/lC2P7WJnQI27Esxl9ItnBw] deleting index
[2022-12-27T00:11:37,913][INFO ][o.e.c.m.MetadataDeleteIndexService] [netology_test] [ind-3/LLnpGgkzQJOLe8XRHiViMg] deleting index
```

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

### Ответ
- Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

> Модифицировал [Dockerfile](./src/Dockerfile) и [elasticsearch.yml](./src/elasticsearch.yml) <br>

<details>

> В текущем образе, что-бы не пересобирать: <br>
> - создал папку `/snapshots`, дал права `777`
> - `echo "path.repo: /opt/elasticsearch-8.2.0/snapshots" >> config/elasticsearch.yml`
> - перезапустил, конечно из образа всё стёрло, волумов не подключал :)
> - пересобрал образ, дабы не тыкать всё руками 

```
# Dockerfile
&& mkdir /opt/elasticsearch-8.2.0/snapshots && chmood -R 777 /opt/elasticsearch-8.2.0/snapshots \
&& chown -R elasticsearch:elasticsearch /opt/elasticsearch-8.2.0/snapshots \

# elasticsearch.yml
path.repo: /opt/elasticsearch-8.2.0/snapshots 
```

</details>

```shell
[vagrant@server65 ~]$ sudo docker build -t 1nxs/elk:0.7.1 . 
[vagrant@server65 ~]$ sudo docker run --rm --name elastic -p 9200:9200 -p 9300:9300 1nxs/elk:0.7.1
[vagrant@server65 ~]$ sudo docker exec -it elastic bash
```
- Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.
- Приведите в ответе запрос API и результат вызова API для создания репозитория.
```shell
# запрос
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic:elastic "https://localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/opt/elasticsearch-8.2.0/snapshots",
    "compress": true
  }
}
'

# ответ
{
  "acknowledged" : true
}
```

- Создайте индекс test с 0 реплик и 1 шардом и приведите в ответе список индексов.
```shell
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic:elastic "https://localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}
# Список индексов
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic:elastic "https://localhost:9200/_cat/indices?v=true"
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  OlPZnRmdSi-MnENrOLiTUQ   1   0          0            0       225b           225b
```
- Создайте snapshot состояния кластера elasticsearch.
```shell
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic:elastic "https://localhost:9200/_snapshot/netology_backup/snapshot_1?wait_for_completion=true&pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "test"
}
'
# ответ
{
  "snapshot" : {
    "snapshot" : "snapshot_1",
    "uuid" : "p-GU2kRQRJy3FKkp-GbhXA",
    "repository" : "netology_backup",
    "version_id" : 8020099,
    "version" : "8.2.0",
    "indices" : [
      ".security-7",
      "test",
      ".geoip_databases"
    ],
    "data_streams" : [ ],
    "include_global_state" : true,
    "state" : "SUCCESS",
    "start_time" : "2022-12-28T17:32:40.010Z",
    "start_time_in_millis" : 1672248760010,
    "end_time" : "2022-12-28T17:32:44.387Z",
    "end_time_in_millis" : 1672248764387,
    "duration_in_millis" : 4377,
    "failures" : [ ],
    "shards" : {
      "total" : 3,
      "failed" : 0,
      "successful" : 3
    },
    "feature_states" : [
      {
        "feature_name" : "geoip",
        "indices" : [
          ".geoip_databases"
        ]
      },
      {
        "feature_name" : "security",
        "indices" : [
          ".security-7"
        ]
      }
    ]
  }
}
```
- Приведите в ответе список файлов в директории со snapshotами.
```shell
[elasticsearch@d480e63dbe74 snapshots]$ ll
total 32
-rw-r--r--. 1 elasticsearch elasticsearch  1095 Dec 28 17:32 index-0
-rw-r--r--. 1 elasticsearch elasticsearch     8 Dec 28 17:32 index.latest
drwxr-xr-x. 5 elasticsearch elasticsearch    96 Dec 28 17:32 indices
-rw-r--r--. 1 elasticsearch elasticsearch 16621 Dec 28 17:32 meta-p-GU2kRQRJy3FKkp-GbhXA.dat
-rw-r--r--. 1 elasticsearch elasticsearch   382 Dec 28 17:32 snap-p-GU2kRQRJy3FKkp-GbhXA.dat
```
- Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.
```shell
[vagrant@server65 ~]$ curl -X DELETE --insecure -u elastic:elastic "https://localhost:9200/test?pretty"
[vagrant@server65 ~]$ curl -X PUT --insecure -u elastic:elastic "https://localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}
'
# Cписок индексов
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic:elastic "https://localhost:9200/_cat/indices?v=true"
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 ciHi28r9Qp6U2ea_n3xqMQ   1   0          0            0       225b           225b
```
- Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.

```shell
# сделаем вид, что первый раз видим задачу и не в курсе о том что есть уже снапшоты
# надобно посмотреть откуда восстанавливаться будем:
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic:elastic "https://localhost:9200/_snapshot/netology_backup/*?verbose=false&pretty"
```
```shell
# восстанавливаем из снапшота индекс `test`
[vagrant@server65 ~]$ curl -X POST --insecure -u elastic:elastic "https://localhost:9200/_snapshot/netology_backup/snapshot_1/_restore?wait_for_completion=true&pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "test"
}
'
# Ответ
{
  "snapshot" : {
    "snapshot" : "snapshot_1",
    "indices" : [
      "test"
    ],
    "shards" : {
      "total" : 1,
      "failed" : 0,
      "successful" : 1
    }
  }
}
```
- Приведите в ответе запрос к API восстановления и итоговый список индексов.
```shell
[vagrant@server65 ~]$ curl -X GET --insecure -u elastic:elastic "https://localhost:9200/_cat/indices?v=true"
health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-2 ciHi28r9Qp6U2ea_n3xqMQ   1   0          0            0       225b           225b
green  open   test   LLFyxc45QpyVitFRaqhmhg   1   0          0            0       225b           225b
```

_Зетс оль, май френдьс :)_

---
_Промежуточные приключения описаны в `<details>`_ 