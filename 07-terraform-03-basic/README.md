# Домашнее задание к занятию "7.3. Основы и принцип работы Терраформ"

## Задача 1. Создадим бэкэнд в S3 (необязательно, но крайне желательно).

Если в рамках предыдущего задания у вас уже есть аккаунт AWS, то давайте продолжим знакомство со взаимодействием
терраформа и aws. 

1. Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ. Можно создать отдельного пользователя,
а можно использовать созданного в рамках предыдущего задания, просто добавьте ему необходимы права, как описано 
[здесь](https://www.terraform.io/docs/backends/types/s3.html).
1. Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше. 


## Задача 2. Инициализируем проект и создаем воркспейсы. 

1. Выполните `terraform init`:
    * если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице 
dynamodb.
    * иначе будет создан локальный файл со стейтами.  
1. Создайте два воркспейса `stage` и `prod`.
1. В уже созданный `aws_instance` добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах 
использовались разные `instance_type`.
1. Добавим `count`. Для `stage` должен создаться один экземпляр `ec2`, а для `prod` два. 
1. Создайте рядом еще один `aws_instance`, но теперь определите их количество при помощи `for_each`, а не `count`.
1. Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр
жизненного цикла `create_before_destroy = true` в один из рессурсов `aws_instance`.
1. При желании поэкспериментируйте с другими параметрами и рессурсами.

В виде результата работы пришлите:
* Вывод команды `terraform workspace list`.
* Вывод команды `terraform plan` для воркспейса `prod`.  

### Ответ
**Задача 1.** Создадим бакет и зарегаем бэкэнд в TF проекте

Изба читальня рекомендует: \
https://cloud.yandex.ru/docs/storage/operations/buckets/create \
https://registry.tfpla.net/providers/yandex-cloud/yandex/latest/docs/resources/storage_bucket

Пробуем воспросизвести для себя \
Создаем бакет:
![virt73-backet.png](img%2Fvirt73-backet.png)

Описываем хранение tfstate [yc-s3.tf](./src/terraform/yc-s3.tf) \
Для всей процедуры нужно соблюсти следующее:
- нужен сервис аккаунт - [мануал](https://cloud.yandex.ru/docs/iam/concepts/users/service-accounts)
- нужны статические ключи доступа для этого сервисного аккаунта, получаем идентификатор и секретный ключ - [мануал](https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key)
- нужен созданный ранее бакет
- корректно записываем все значения в [yc-s3.tf](./src/terraform/yc-s3.tf) - [мануал](https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-state-storage#configure-provider)
- `terraform init -backend-config="access_key=<KEY>" -backend-config="secret_key=<KEY>"`\
в моём случае, тк до этого уже был многократный инит \
`❯ terraform init -backend-config=static.key -reconfigure`

![tfstate.png](img%2Ftfstate.png)

**Задача 2** 
- **Часть 1**
1. Выполните `terraform init`:
    * если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице 
dynamodb.
    * иначе будет создан локальный файл со стейтами.  
> Выполнено в рамках **Задачи 1**
- **Часть 2**
2. Создайте два воркспейса `stage` и `prod`.
```shell
❯ terraform workspace new stage
Created and switched to workspace "stage"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.

❯ terraform workspace new prod
Created and switched to workspace "prod"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
```
![workspace-env.png](img%2Fworkspace-env.png)

- **Часть 3**
3. В уже созданный `aws_instance` добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах 
использовались разные `instance_type`.
1. Добавим `count`. Для `stage` должен создаться один экземпляр `ec2`, а для `prod` два. 
1. Создайте рядом еще один `aws_instance`, но теперь определите их количество при помощи `for_each`, а не `count`.
1. Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр
жизненного цикла `create_before_destroy = true` в один из рессурсов `aws_instance`.
1. При желании поэкспериментируйте с другими параметрами и рессурсами.

В виде результата работы пришлите:
* Вывод команды `terraform workspace list`.
* Вывод команды `terraform plan` для воркспейса `prod`.  

Продолжаем адаптировать задачи под Yandex.Cloud:

- В Packer подготавим образ Centos7 [centos-7-base.json](src%2Fpacker%2Fcentos-7-base.json)
```shell
packer build centos-7-base.json
```
![img-build.png](img%2Fimg-build.png)

- Описываем задачу в [main.tf](src%2Fterraform%2Fmain.tf)

- Вывод команды `terraform workspace list`.
```
❯ terraform workspace list
  default
  prod
* stage
```
- Вывод команды `terraform plan` для воркспейса `prod`. 
```shell
❯ terraform workspace select prod
Switched to workspace "prod".
❯ terraform plan >> tf-plan.log 
```

---
> все материалы собраны в рамках текущего задания, каталог `src`