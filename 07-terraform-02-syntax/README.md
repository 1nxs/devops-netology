# Домашнее задание к занятию "7.2. Облачные провайдеры и синтаксис Terraform."

Зачастую разбираться в новых инструментах гораздо интересней понимая то, как они работают изнутри. 
Поэтому в рамках первого *необязательного* задания предлагается завести свою учетную запись в AWS (Amazon Web Services) или Yandex.Cloud.
Идеально будет познакомится с обоими облаками, потому что они отличаются. 

## Задача 1 (вариант с AWS). Регистрация в aws и знакомство с основами (необязательно, но крайне желательно).

Остальные задания можно будет выполнять и без этого аккаунта, но с ним можно будет увидеть полный цикл процессов. 

AWS предоставляет достаточно много бесплатных ресурсов в первый год после регистрации, подробно описано [здесь](https://aws.amazon.com/free/).
1. Создайте аккаут aws.
1. Установите c aws-cli https://aws.amazon.com/cli/.
1. Выполните первичную настройку aws-sli https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html.
1. Создайте IAM политику для терраформа c правами
    * AmazonEC2FullAccess
    * AmazonS3FullAccess
    * AmazonDynamoDBFullAccess
    * AmazonRDSFullAccess
    * CloudWatchFullAccess
    * IAMFullAccess
1. Добавьте переменные окружения 
    ```
    export AWS_ACCESS_KEY_ID=(your access key id)
    export AWS_SECRET_ACCESS_KEY=(your secret access key)
    ```
1. Создайте, остановите и удалите ec2 инстанс (любой с пометкой `free tier`) через веб интерфейс. 

В виде результата задания приложите вывод команды `aws configure list`.

## Задача 1 (Вариант с Yandex.Cloud). Регистрация в ЯО и знакомство с основами (необязательно, но крайне желательно).

1. Подробная инструкция на русском языке содержится [здесь](https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart).
2. Обратите внимание на период бесплатного использования после регистрации аккаунта. 
3. Используйте раздел "Подготовьте облако к работе" для регистрации аккаунта. Далее раздел "Настройте провайдер" для подготовки
базового терраформ конфига.
4. Воспользуйтесь [инструкцией](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs) на сайте терраформа, что бы 
не указывать авторизационный токен в коде, а терраформ провайдер брал его из переменных окружений.

## Задача 2. Создание aws ec2 или yandex_compute_instance через терраформ. 

1. В каталоге `terraform` вашего основного репозитория, который был создан в начале курсе, создайте файл `main.tf` и `versions.tf`.
2. Зарегистрируйте провайдер 
   1. для [aws](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). В файл `main.tf` добавьте
   блок `provider`, а в `versions.tf` блок `terraform` с вложенным блоком `required_providers`. Укажите любой выбранный вами регион 
   внутри блока `provider`.
   2. либо для [yandex.cloud](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs). Подробную инструкцию можно найти 
   [здесь](https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart).
3. Внимание! В гит репозиторий нельзя пушить ваши личные ключи доступа к аккаунту. Поэтому в предыдущем задании мы указывали
их в виде переменных окружения. 
4. В файле `main.tf` воспользуйтесь блоком `data "aws_ami` для поиска ami образа последнего Ubuntu.  
5. В файле `main.tf` создайте рессурс 
   1. либо [ec2 instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance).
   Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров указан в первом блоке 
   `Example Usage`, но желательно, указать большее количество параметров.
   2. либо [yandex_compute_image](https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs/resources/compute_image).
6. Также в случае использования aws:
   1. Добавьте data-блоки `aws_caller_identity` и `aws_region`.
   2. В файл `outputs.tf` поместить блоки `output` с данными об используемых в данный момент: 
       * AWS account ID,
       * AWS user ID,
       * AWS регион, который используется в данный момент, 
       * Приватный IP ec2 инстансы,
       * Идентификатор подсети в которой создан инстанс.  
7. Если вы выполнили первый пункт, то добейтесь того, что бы команда `terraform plan` выполнялась без ошибок. 


В качестве результата задания предоставьте:
1. Ответ на вопрос: при помощи какого инструмента (из разобранных на прошлом занятии) можно создать свой образ ami?
1. Ссылку на репозиторий с исходной конфигурацией терраформа.  


### Ответ
Всё задание будет выполняться на базе Yandex.Cloud.\
**Задача 1** уже была выполнена в рамках занятия "4. Оркестрация группой Docker контейнеров на примере Docker Compose"
```shell
❯ yc config list
token: вот-тут-токен-который-нельзя-светить
cloud-id: b1gn303gl4s828djdqfi
folder-id: b1gprhi83f991tp8b54f
compute-default-zone: ru-central1-a
# посмотрим на сервис-аккаунты
❯ yc iam service-account list
+----------------------+--------+
|          ID          |  NAME  |
+----------------------+--------+
| aje2s81v97s1ev7s3rb3 | takari |
+----------------------+--------+
# ключ >> key.json
❯ yc iam key create --service-account-name takari --output key.json
```
Образ мы будем создавать через `Packer` \
[centos-7-base.json](./src/packer/centos-7-base-wo-key.json)
```shell
❯ packer inspect centos-7-base.json
❯ packer build centos-7-base.json
yandex: output will be in this color.

==> yandex: Creating temporary RSA SSH key for instance...
==> yandex: Using as source image: fd8jvcoeij6u9se84dt5 (name: "centos-7-v20221121", family: "centos-7")
==> yandex: Creating network...
==> yandex: Creating subnet in zone "ru-central1-a"...
==> yandex: Creating disk...
==> yandex: Creating instance...
# -----
Build 'yandex' finished after 5 minutes 529 milliseconds.

==> Wait completed after 5 minutes 530 milliseconds

==> Builds finished. The artifacts of successful builds are:
--> yandex: A disk image was created: centos-7-base (id: fd8hu92egb4b7or9b4gh) with family name centos
```
Теперь инициализируем провайдера
```shell
❯ terraform init
Initializing the backend...

Initializing provider plugins...
- Finding latest version of yandex-cloud/yandex...
- Installing yandex-cloud/yandex v0.84.0...
Terraform has been successfully initialized!
```
Если вы выполнили первый пункт, то добейтесь того, что бы команда `terraform plan` выполнялась без ошибок

<details><summary>вывод terraform plan</summary>

```shell
❯ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.srv72-01 will be created
  + resource "yandex_compute_instance" "srv72-01" {
      + allow_stopping_for_update = true
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = "srv72-01.netology.lab"
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                centos:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCWto6eDr35F0CgjCUDe/WjSrYAdXDfNOlXcjh8owYRBN9A0E7rcQuRtxvUPO4OYARO6okeKjUQ4Pg07zmrLINFHXybo6Hg1KRU43z23+jjA3HX4GFD1QFaK7c5/YO6hZK6v7GS85pAcMmCibsvgeRISJ2+/ZKy3bfpGACrbYRcaA7O+nxzTcvcKIouc0P9cne9FBOQK6bb60uzQWNCbH7zlyJcoXrugaa44kOWscuP6dCpfSEGlEY7BVSNOU1K0ereAoFfmCd6u3eLvj8LEKw/WWS2UUNW/QggbEfIcRyts0QBzltUl4NmCOEV6s+pTxgIk5KBWVHz7fmQL5afhnwrR2PjkFec1DfWpECFDIp2Vt+GfLm80foW/C/8ybM3+zc2lJW2Y83YpoMncaC4GppE5yKIqDut92dOWOvr0Ppv4teHep0D/goX/4xco+zr4m/B2nhMujqskPsIDj1XrWDnZD047f2uhy7Bkj9n+YiDWGCNPiOBJjtMDfsIDjfVCHlvr9wPPrJrNOB42/K76lKsl7sWvF3TAiOIupi7T8nJGJciRYq/hz9e4qOZdq1rCmPJOuCzdPi58pH1WFadsbambA+YG7f34phuD5mfz+geRNFkAbkeSqfARoThVR02oUVnWAIu+edPWvuxPEDLikWd6vEhGm8t6wDf61v/ZHJg5Q== yakushin.pavel@gmail.com
            EOT
        }
      + name                      = "srv72-01"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = "ru-central1-a"

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd8hu92egb4b7or9b4gh"
              + name        = "root-srv72-01"
              + size        = 50
              + snapshot_id = (known after apply)
              + type        = "network-nvme"
            }
        }

      + metadata_options {
          + aws_v1_http_endpoint = (known after apply)
          + aws_v1_http_token    = (known after apply)
          + gce_http_endpoint    = (known after apply)
          + gce_http_token       = (known after apply)
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 100
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_vpc_network.default will be created
  + resource "yandex_vpc_network" "default" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "net"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_subnet.default will be created
  + resource "yandex_vpc_subnet" "default" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.10.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-a"
    }

Plan: 3 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + external_ip_address_srv72-01_yandex_cloud = (known after apply)
  + internal_ip_address_srv72-01_yandex_cloud = (known after apply)
```
</details>

Отправляем Terraform работать с YC, применение конфигурации в облаке на основе образа сделанного в Packer
<details><summary>вывод terraform apply</summary>

```shell
❯ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.srv72-01 will be created
  + resource "yandex_compute_instance" "srv72-01" {
      + allow_stopping_for_update = true
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = "srv72-01.netology.lab"
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                centos:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCWto6eDr35F0CgjCUDe/WjSrYAdXDfNOlXcjh8owYRBN9A0E7rcQuRtxvUPO4OYARO6okeKjUQ4Pg07zmrLINFHXybo6Hg1KRU43z23+jjA3HX4GFD1QFaK7c5/YO6hZK6v7GS85pAcMmCibsvgeRISJ2+/ZKy3bfpGACrbYRcaA7O+nxzTcvcKIouc0P9cne9FBOQK6bb60uzQWNCbH7zlyJcoXrugaa44kOWscuP6dCpfSEGlEY7BVSNOU1K0ereAoFfmCd6u3eLvj8LEKw/WWS2UUNW/QggbEfIcRyts0QBzltUl4NmCOEV6s+pTxgIk5KBWVHz7fmQL5afhnwrR2PjkFec1DfWpECFDIp2Vt+GfLm80foW/C/8ybM3+zc2lJW2Y83YpoMncaC4GppE5yKIqDut92dOWOvr0Ppv4teHep0D/goX/4xco+zr4m/B2nhMujqskPsIDj1XrWDnZD047f2uhy7Bkj9n+YiDWGCNPiOBJjtMDfsIDjfVCHlvr9wPPrJrNOB42/K76lKsl7sWvF3TAiOIupi7T8nJGJciRYq/hz9e4qOZdq1rCmPJOuCzdPi58pH1WFadsbambA+YG7f34phuD5mfz+geRNFkAbkeSqfARoThVR02oUVnWAIu+edPWvuxPEDLikWd6vEhGm8t6wDf61v/ZHJg5Q== yakushin.pavel@gmail.com
            EOT
        }
      + name                      = "srv72-01"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = "ru-central1-a"

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd8hu92egb4b7or9b4gh"
              + name        = "root-srv72-01"
              + size        = 50
              + snapshot_id = (known after apply)
              + type        = "network-nvme"
            }
        }

      + metadata_options {
          + aws_v1_http_endpoint = (known after apply)
          + aws_v1_http_token    = (known after apply)
          + gce_http_endpoint    = (known after apply)
          + gce_http_token       = (known after apply)
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 100
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_vpc_network.default will be created
  + resource "yandex_vpc_network" "default" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "net"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_subnet.default will be created
  + resource "yandex_vpc_subnet" "default" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.10.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-a"
    }

Plan: 3 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + external_ip_address_srv72-01_yandex_cloud = (known after apply)
  + internal_ip_address_srv72-01_yandex_cloud = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

yandex_vpc_network.default: Creating...
yandex_vpc_network.default: Creation complete after 2s [id=enp730m8en1e6p8h3kn1]
yandex_vpc_subnet.default: Creating...
yandex_vpc_subnet.default: Creation complete after 0s [id=e9b9d7konlf0lhstqom4]
yandex_compute_instance.srv72-01: Creating...
yandex_compute_instance.srv72-01: Still creating... [10s elapsed]
yandex_compute_instance.srv72-01: Still creating... [20s elapsed]
yandex_compute_instance.srv72-01: Still creating... [30s elapsed]
yandex_compute_instance.srv72-01: Still creating... [40s elapsed]
yandex_compute_instance.srv72-01: Still creating... [50s elapsed]
yandex_compute_instance.srv72-01: Creation complete after 55s [id=fhmeruva9ragtrlakukt]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

external_ip_address_srv72-01_yandex_cloud = "51.250.0.87"
internal_ip_address_srv72-01_yandex_cloud = "192.168.10.16"
```
</details>

Дабы не тратить ~~деньги в пустую~~ ресурсы облака без необходимости, прибираемся за собой

<details><summary>вывод terraform destroy</summary>

```shell
❯ terraform destroy -auto-approve
yandex_vpc_network.default: Refreshing state... [id=enp730m8en1e6p8h3kn1]
yandex_vpc_subnet.default: Refreshing state... [id=e9b9d7konlf0lhstqom4]
yandex_compute_instance.srv72-01: Refreshing state... [id=fhmeruva9ragtrlakukt]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # yandex_compute_instance.srv72-01 will be destroyed
  - resource "yandex_compute_instance" "srv72-01" {
      - allow_stopping_for_update = true -> null
      - created_at                = "2023-01-04T19:20:44Z" -> null
      - folder_id                 = "b1gprhi83f991tp8b54f" -> null
      - fqdn                      = "srv72-01.netology.lab" -> null
      - hostname                  = "srv72-01.netology.lab" -> null
      - id                        = "fhmeruva9ragtrlakukt" -> null
      - labels                    = {} -> null
      - metadata                  = {
          - "ssh-keys" = <<-EOT
                centos:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCWto6eDr35F0CgjCUDe/WjSrYAdXDfNOlXcjh8owYRBN9A0E7rcQuRtxvUPO4OYARO6okeKjUQ4Pg07zmrLINFHXybo6Hg1KRU43z23+jjA3HX4GFD1QFaK7c5/YO6hZK6v7GS85pAcMmCibsvgeRISJ2+/ZKy3bfpGACrbYRcaA7O+nxzTcvcKIouc0P9cne9FBOQK6bb60uzQWNCbH7zlyJcoXrugaa44kOWscuP6dCpfSEGlEY7BVSNOU1K0ereAoFfmCd6u3eLvj8LEKw/WWS2UUNW/QggbEfIcRyts0QBzltUl4NmCOEV6s+pTxgIk5KBWVHz7fmQL5afhnwrR2PjkFec1DfWpECFDIp2Vt+GfLm80foW/C/8ybM3+zc2lJW2Y83YpoMncaC4GppE5yKIqDut92dOWOvr0Ppv4teHep0D/goX/4xco+zr4m/B2nhMujqskPsIDj1XrWDnZD047f2uhy7Bkj9n+YiDWGCNPiOBJjtMDfsIDjfVCHlvr9wPPrJrNOB42/K76lKsl7sWvF3TAiOIupi7T8nJGJciRYq/hz9e4qOZdq1rCmPJOuCzdPi58pH1WFadsbambA+YG7f34phuD5mfz+geRNFkAbkeSqfARoThVR02oUVnWAIu+edPWvuxPEDLikWd6vEhGm8t6wDf61v/ZHJg5Q== yakushin.pavel@gmail.com
            EOT
        } -> null
      - name                      = "srv72-01" -> null
      - network_acceleration_type = "standard" -> null
      - platform_id               = "standard-v1" -> null
      - status                    = "running" -> null
      - zone                      = "ru-central1-a" -> null

      - boot_disk {
          - auto_delete = true -> null
          - device_name = "fhmvvrcv2tts4jgjt6ic" -> null
          - disk_id     = "fhmvvrcv2tts4jgjt6ic" -> null
          - mode        = "READ_WRITE" -> null

          - initialize_params {
              - block_size = 4096 -> null
              - image_id   = "fd8hu92egb4b7or9b4gh" -> null
              - name       = "root-srv72-01" -> null
              - size       = 50 -> null
              - type       = "network-ssd" -> null
            }
        }

      - metadata_options {
          - aws_v1_http_endpoint = 1 -> null
          - aws_v1_http_token    = 1 -> null
          - gce_http_endpoint    = 1 -> null
          - gce_http_token       = 1 -> null
        }

      - network_interface {
          - index              = 0 -> null
          - ip_address         = "192.168.10.16" -> null
          - ipv4               = true -> null
          - ipv6               = false -> null
          - mac_address        = "d0:0d:ed:fb:ea:4e" -> null
          - nat                = true -> null
          - nat_ip_address     = "51.250.0.87" -> null
          - nat_ip_version     = "IPV4" -> null
          - security_group_ids = [] -> null
          - subnet_id          = "e9b9d7konlf0lhstqom4" -> null
        }

      - placement_policy {
          - host_affinity_rules = [] -> null
        }

      - resources {
          - core_fraction = 100 -> null
          - cores         = 2 -> null
          - gpus          = 0 -> null
          - memory        = 2 -> null
        }

      - scheduling_policy {
          - preemptible = false -> null
        }
    }

  # yandex_vpc_network.default will be destroyed
  - resource "yandex_vpc_network" "default" {
      - created_at = "2023-01-04T19:20:42Z" -> null
      - folder_id  = "b1gprhi83f991tp8b54f" -> null
      - id         = "enp730m8en1e6p8h3kn1" -> null
      - labels     = {} -> null
      - name       = "net" -> null
      - subnet_ids = [
          - "e9b9d7konlf0lhstqom4",
        ] -> null
    }

  # yandex_vpc_subnet.default will be destroyed
  - resource "yandex_vpc_subnet" "default" {
      - created_at     = "2023-01-04T19:20:43Z" -> null
      - folder_id      = "b1gprhi83f991tp8b54f" -> null
      - id             = "e9b9d7konlf0lhstqom4" -> null
      - labels         = {} -> null
      - name           = "subnet" -> null
      - network_id     = "enp730m8en1e6p8h3kn1" -> null
      - v4_cidr_blocks = [
          - "192.168.10.0/24",
        ] -> null
      - v6_cidr_blocks = [] -> null
      - zone           = "ru-central1-a" -> null
    }

Plan: 0 to add, 0 to change, 3 to destroy.

Changes to Outputs:
  - external_ip_address_srv72-01_yandex_cloud = "51.250.0.87" -> null
  - internal_ip_address_srv72-01_yandex_cloud = "192.168.10.16" -> null
yandex_compute_instance.srv72-01: Destroying... [id=fhmeruva9ragtrlakukt]
yandex_compute_instance.srv72-01: Still destroying... [id=fhmeruva9ragtrlakukt, 10s elapsed]
yandex_compute_instance.srv72-01: Still destroying... [id=fhmeruva9ragtrlakukt, 20s elapsed]
yandex_compute_instance.srv72-01: Destruction complete after 22s
yandex_vpc_subnet.default: Destroying... [id=e9b9d7konlf0lhstqom4]
yandex_vpc_subnet.default: Destruction complete after 3s
yandex_vpc_network.default: Destroying... [id=enp730m8en1e6p8h3kn1]
yandex_vpc_network.default: Destruction complete after 0s

Destroy complete! Resources: 3 destroyed.
```
</details>

Остается прибрать за собой образ Packer
```shell
yc compute images delete --name centos-7-base
```
В качестве результата задания предоставьте [**ссылку**](./src/terraform) на репозиторий с исходной конфигурацией терраформа.
> все материалы собраны в рамках текущего задания, каталог `src`