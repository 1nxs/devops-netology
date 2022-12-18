
# Домашнее задание к занятию "3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```html
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

### Ответ
<details>

```shell
vagrant@server1:~/nginx$
# Prepare Dockerfile 4 build
$ touch Dockerfile
$ nano Dockerfile 
$ cat Dockerfile 
FROM nginx:latest
COPY ./index.html /usr/share/nginx/html/index.html
# Prepare index.html 4 nginx
$ touch index.html
$ nano index.html 
$ cat index.html 
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
# Docker build
$ docker build -t 1nxs/nginx .
Sending build context to Docker daemon  3.072kB
Step 1/2 : FROM nginx:latest
latest: Pulling from library/nginx
e9995326b091: Pull complete 
71689475aec2: Pull complete 
f88a23025338: Pull complete 
0df440342e26: Pull complete 
eef26ceb3309: Pull complete 
8e3ed6a9e43a: Pull complete 
Digest: sha256:943c25b4b66b332184d5ba6bb18234273551593016c0e0ae906bab111548239f
Status: Downloaded newer image for nginx:latest
 ---> 76c69feac34e
Step 2/2 : COPY ./index.html /usr/share/nginx/html/index.html
 ---> 083518b0b543
Successfully built 083518b0b543
Successfully tagged 1nxs/nginx:latest
# Run to test
$ docker run -it -d -p 8080:80 --name nginx 1nxs/nginx:latest
9bcfd0d2020b15eb7697620b082246e73363ba5feb67bd4364fd82cec455a762

$ docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED       STATUS       PORTS                                   NAMES
9bcfd0d2020b   1nxs/nginx:latest   "/docker-entrypoint.…"   2 hours ago   Up 2 hours   0.0.0.0:8080->80/tcp, :::8080->80/tcp   nginx
# It's alive :)
$ curl 0.0.0.0:8080
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>

# Prepare to deploy
# Add tag
$ docker tag 1nxs/nginx 1nxs/nginx:1.0
$ docker images -a
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
1nxs/nginx   1.0       083518b0b543   2 hours ago   142MB
1nxs/nginx   latest    083518b0b543   2 hours ago   142MB
nginx        latest    76c69feac34e   2 weeks ago   142MB

# Push to hub.docker.com
$  docker login -u 1nxs
$  docker push 1nxs/nginx:1.0
```
</details>

- https://hub.docker.com/repository/docker/1nxs/nginx

## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
- Nodejs веб-приложение;
- Мобильное приложение c версиями для Android и iOS;
- Шина данных на базе Apache Kafka;
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
- Мониторинг-стек на базе Prometheus и Grafana;
- MongoDB, как основное хранилище данных для java-приложения;
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.

### Ответ
- Высоконагруженное монолитное java веб-приложение;
  - Ну монолитное java - это ключевое, Java будет юзать JVM. Так что контейнеры тут лишние, просто виртуалка будет правильнее.
- Nodejs веб-приложение;
  - Вот тут как раз обратная ситуация. Docker даст удобство для разработки - быстро много копий, возможность масштабироваться и переноса.
- Мобильное приложение c версиями для Android и iOS;
  - Ну для Дроида есть что-то похожее на докер, для IOS нет его.
- Шина данных на базе Apache Kafka;
  - Подходит, можно использовать для масштабирования. Для среды тестировки еще, чтоб шина прода "не страдала" :)
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
  - Вендор рекомендует, да и в целом можно, накладные расходы не большие от контейнеров
- Мониторинг-стек на базе Prometheus и Grafana;
  - Так-же, подходит. Удобно пока идёт активная настройка в т.ч.
- MongoDB, как основное хранилище данных для java-приложения;
  - Ну, в целом для db не рекомендуется в прод, но для маленьких или тестовых подходит.
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.
  - А зачем? Изменения в таких машинах минимальны, а вот данных там обычно много, в случае Registry - там еще и файлики могут быть крайне жирными.\
  - В контейнер тоже можно, а вот данные с него нужно мапить.


## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.

### Ответ
```shell
$ sudo mkdir data
$ docker run -it -d --name centos --mount type=bind,source=/data,target=/data centos
$ docker run -it -d --name debian --mount type=bind,source=/data,target=/data debian
$ docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                   NAMES
132df8fb3e01   debian              "bash"                   51 seconds ago   Up 49 seconds                                           debian
75d0324c4ea1   centos              "/bin/bash"              2 minutes ago    Up 2 minutes                                            centos
$ docker exec -it centos bash
[root@75d0324c4ea1 /]# touch /data/42_centos.txt
[root@75d0324c4ea1 /]# vi /data/42_centos.txt
$ docker exec -it debian bash     
root@132df8fb3e01:/# touch /data/42_debian.txt
root@132df8fb3e01:/# ls -la /data/
total 16
drwxr-xr-x 2 root root 4096 Nov 11 18:08 .
drwxr-xr-x 1 root root 4096 Nov 11 17:58 ..
-rw-r--r-- 1 root root   56 Nov 11 18:04 42.txt
-rw-r--r-- 1 root root   56 Nov 11 18:07 42_centos.txt
-rw-r--r-- 1 root root    0 Nov 11 18:08 42_debian.txt
root@132df8fb3e01:/# cat /data/42_centos.txt 
ultimate question of life, the universe, and everything
```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.

### Ответ

- https://hub.docker.com/repository/docker/1nxs/ansible
> сделал dockerfile \
> собрал образ, выставил тэг \
> закинул в hub.docker
