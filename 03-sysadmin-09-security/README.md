# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

1. Установите Bitwarden плагин для браузера. Зарегестрируйтесь и сохраните несколько паролей.

2. Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden акаунт через Google authenticator OTP.

3. Установите apache2, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.
```shell
vagrant@vagrant:~$ sudo apt install apache2
vagrant@vagrant:~$ sudo openssl req -x509 -nodes -days 90 -newkey rsa:2048 -keyout /etc/ssl/private/ap                                                                                                 ache-selfsigned.key -out /etc/ssl/private/apache-selfsigned.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=MyCompany/OU=ORG/CN=www.nowhere.com"ache-selfsigned.key -out /etc/ssl/private/apache-selfsigned.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=MyCompany/OU=ORG/CN=www.nowhere.com"
vagrant@vagrant:~$ sudo ls -la /etc/ssl/private/
-rw-r--r-- 1 root root     1350 Oct 14 19:06 apache-selfsigned.crt
-rw------- 1 root root     1704 Oct 14 19:06 apache-selfsigned.key
vagrant@vagrant:~$ sudo vi /etc/apache2/conf-available/ssl-params.conf
#---
vagrant@vagrant:~$ sudo cat /etc/apache2/conf-available/ssl-params.conf
SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
SSLProtocol All -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
SSLHonorCipherOrder On
# Disable preloading HSTS for now.  You can use the commented out header line that includes
# the "preload" directive if you understand the implications.
# Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
Header always set X-Frame-Options DENY
Header always set X-Content-Type-Options nosniff
# Requires Apache >= 2.4
SSLCompression off
SSLUseStapling on
SSLStaplingCache "shmcb:logs/stapling-cache(150000)"
# Requires Apache >= 2.4.11
SSLSessionTickets Off
#---
vagrant@vagrant:~$ sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf.bak
vagrant@vagrant:~$ sudo vi /etc/apache2/sites-available/default-ssl.conf
vagrant@vagrant:~$ sudo -i
root@vagrant:# a2enmod ssl
root@vagrant:# a2enmod headers
root@vagrant:# a2ensite default-ssl
root@vagrant:# a2enconf ssl-params
root@vagrant:# apache2ctl configtest
root@vagrant:# sudo apache2ctl configtest
AH00558: apache2: Could not reliably determine the server fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
Syntax OK
root@vagrant:# systemctl restart apache2
```
4. Проверьте на TLS уязвимости произвольный сайт в интернете (кроме сайтов МВД, ФСБ, МинОбр, НацБанк, РосКосмос, РосАтом, РосНАНО и любых госкомпаний, объектов КИИ, ВПК ... и тому подобное).
```shell
vagrant@vagrant:~$ git clone --depth 1 https://github.com/drwetter/testssl.sh.git
vagrant@vagrant:~$ cd testssl.sh
vagrant@vagrant:~/testssl.sh$  ./testssl.sh https://www.google.com/
```

5. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.
```shell
vagrant@vagrant:~/testssl.sh$ ssh-keygen -C "yakushin.pavel+netology@gmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/vagrant/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/vagrant/.ssh/id_rsa
Your public key has been saved in /home/vagrant/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:--- yakushin.pavel+netology@gmail.com
The key's randomart image is:
+---[RSA 3072]----+
|      .o.o. . .  |
|        +.+. + . |
|       ..=.+o =  |
|      ..+ .+.o .o|
|       +S. .+   +|
|      = . .+ o ..|
|     + o  ..B.B .|
|    E o  o.=.O.o |
|         o= +.   |
+----[SHA256]-----+
```

```shell
# До добавления отпечатка в github
vagrant@vagrant:~/testssl.sh$ ssh -T git@github.com
git@github.com: Permission denied (publickey).
# после добавления отпечатка в github
vagrant@vagrant:~$ cat ~/.ssh/id_rsa.pub
ssh-rsa ***qh+GeneRvEc+ycOOKgHjnS8rN++++boj+vFNg9bJ2tL6***vsGYwi46W0= yakushin.pavel+netology@gmail.com
vagrant@vagrant:~h$ ssh -T git@github.com
Hi 1nxs! You've successfully authenticated, but GitHub does not provide shell access.
```
6. Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.

```shell
vagrant@vagrant:~$ mv ~/.ssh/id_rsa ~/.ssh/id_rsa_git
vagrant@vagrant:~$ ls ~/.ssh/
authorized_keys  id_rsa_git       id_rsa.pub       known_hosts      known_hosts.old
vagrant@vagrant:~$ vi ~/.ssh/config
vagrant@vagrant:~$ cat ~/.ssh/config
Host githab
  HostName github.com
  IdentityFile ~/.ssh/id_rsa_git
  User git
vagrant@vagrant:~$ ssh githab
PTY allocation request failed on channel 0
Hi 1nxs! You`ve successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed.
vagrant@vagrant:~$
```

7. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.

 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

8*. Просканируйте хост scanme.nmap.org. Какие сервисы запущены?

9*. Установите и настройте фаервол ufw на web-сервер из задания 3. Откройте доступ снаружи только к портам 22,80,443


 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате учебной группы.

---

