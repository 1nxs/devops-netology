# Домашнее задание к занятию "3. Использование Yandex Cloud"

## Подготовка к выполнению

1. Подготовьте в Yandex Cloud три хоста: для `clickhouse`, для `vector` и для `lighthouse`.

Ссылка на репозиторий LightHouse: https://github.com/VKCOM/lighthouse

## Основная часть

1. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает lighthouse.
2. При создании tasks рекомендую использовать модули: `get_url`, `template`, `yum`, `apt`.
3. Tasks должны: скачать статику lighthouse, установить nginx или любой другой webserver, настроить его конфиг для открытия lighthouse, запустить webserver.
4. Приготовьте свой собственный inventory файл `prod.yml`.
5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-03-yandex` на фиксирующий коммит, в ответ предоставьте ссылку на него.

---
## Ответ
0. Подготовка стека:
   * Prod - `prod.yml`
      - Vagrant
        - [vagrantfile](src/vagrantfile)
      - Ansible
        - [Inventory](src/ansible/inventory/prod.yml) 
        - [provision.yml](src/ansible/provision.yml)
        
   * Yandex Cloud - `yc.yml`
     - Три машины на YC - без использования Terraform
     - Ansible
       - [Inventory](src/ansible/inventory/yc.yml) 
1. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает lighthouse.
   * В playbook [site.yml](src/ansible/site.yml) дописан еще один `play`
   * Дописаны [конфигурационные файлы](src/ansible/templates) для настройки сервисов 
   * Созданы необходимые [group_vars](src/ansible/group_vars)
2. Подготовьте README.md файл по своему playbook. <br>
В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
   - [README.md](src/ansible/README.md) - Описание
   - [site.yml](src/ansible/site.yml) - Playbook
   - [src](src) - Рабочая директория со всеми материалами по домашнему заданию
3. Установить тег `08-ansible-03-yandex`
