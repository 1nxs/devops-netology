
# Домашнее задание к занятию "2. Применение принципов IaaC в работе с виртуальными машинами"

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
> Исключение человеческого фактора, путем автоматизации мах возможных процессов.\
> Масштабируемость и скорость развертки сервисов. Прогнозируемость и повторяемость результата. Возможность быстрого восстановления инфраструктуры. Документация
- Какой из принципов IaaC является основополагающим?
> Идемпотетность - получение идентичного, гарантированного результата при многих повторных операциях исполнения конфигурации.

## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
> Тем, что не требуется расставлять отдельных агентов, тк используется SSH. Достаточно удобная структура конфигурации. Community + большое кол-во готовых модулей. Ну и "любимый" yaml в коплекте..
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?
> Не совсем корректная постановка вопроса, тк зависит от задачи. \
> Отличие только в инициаторе, и при нарушении канала связи оба метода буду неработоспособными.
> - Метод push - более централизован и удобен для развертывания "одинаковых" систем.
> - Метод pull - хост получает свою конфигурацию, что позволяет раздельные кастомизации.
## Задача 3

Установить на личный компьютер:

- VirtualBox
```shell
inxs@geata:~/vagrant$ echo $(vboxmanage --version)
6.1.38_Ubuntur153438
```
- Vagrant
```shell
inxs@geata:~/vagrant$ echo $(vagrant --version)
Vagrant 2.3.2
```
- Ansible
```shell
inxs@geata:~/vagrant$ echo $(ansible --version)
ansible 2.10.8
```

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.
- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
```
docker ps
```
```shell
inxs@geata:~/vagrant$ vagrant ssh
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-110-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 08 Nov 2022 07:57:05 PM UTC

  System load:  0.0                Users logged in:          0
  Usage of /:   13.1% of 30.63GB   IPv4 address for docker0: 172.17.0.1
  Memory usage: 23%                IPv4 address for eth0:    10.0.2.15
  Swap usage:   0%                 IPv4 address for eth1:    192.168.56.11
  Processes:    108


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Tue Nov  8 19:23:20 2022 from 10.0.2.2
vagrant@server1:~$ sudo docker -v && docker ps
Docker version 20.10.21, build baeda1f
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
vagrant@server1:~$ 
```