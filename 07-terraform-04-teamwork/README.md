# Домашнее задание к занятию "7.4. Средства командной работы над инфраструктурой."

## Задача 1. Настроить terraform cloud (необязательно, но крайне желательно).

В это задании предлагается познакомиться со средством командой работы над инфраструктурой предоставляемым
разработчиками терраформа. 

1. Зарегистрируйтесь на [https://app.terraform.io/](https://app.terraform.io/).
(регистрация бесплатная и не требует использования платежных инструментов).
1. Создайте в своем github аккаунте (или другом хранилище репозиториев) отдельный репозиторий с
 конфигурационными файлами прошлых занятий (или воспользуйтесь любым простым конфигом).
1. Зарегистрируйте этот репозиторий в [https://app.terraform.io/](https://app.terraform.io/).
1. Выполните plan и apply. 

В качестве результата задания приложите снимок экрана с успешным применением конфигурации.

### Ответ
1. Зарегистрировался
2. Отдельный репо с файлами - https://github.com/1nxs/07-terraform-04-teamwork
3. Создан workspace >> добавлен репо из п.2
4. Результаты:
**Terraform Cloud** \
![tfc-plan-apply.png](img%2Ftfc-plan-apply.png)
**Yandex Cloud** \
![tfc-yc-push-vm.png](img%2Ftfc-yc-push-vm.png)
## Задача 2. Написать серверный конфиг для атлантиса. 

Смысл задания – познакомиться с документацией 
о [серверной](https://www.runatlantis.io/docs/server-side-repo-config.html) конфигурации и конфигурации уровня 
 [репозитория](https://www.runatlantis.io/docs/repo-level-atlantis-yaml.html).

Создай `server.yaml` который скажет атлантису:
1. Укажите, что атлантис должен работать только для репозиториев в вашем github (или любом другом) аккаунте.
1. На стороне клиентского конфига разрешите изменять `workflow`, то есть для каждого репозитория можно 
будет указать свои дополнительные команды. 
1. В `workflow` используемом по-умолчанию сделайте так, что бы во время планирования не происходил `lock` состояния.

Создай `atlantis.yaml` который, если поместить в корень terraform проекта, скажет атлантису:
1. Надо запускать планирование и аплай для двух воркспейсов `stage` и `prod`.
1. Необходимо включить автопланирование при изменении любых файлов `*.tf`.

В качестве результата приложите ссылку на файлы `server.yaml` и `atlantis.yaml`.

### Ответ
1. Собираем стек для Atlantis
Традиционно - `Vagrant+Ansible+Docker`
2. Читаем доки по [деплою](https://www.runatlantis.io/docs/deployment.html#docker) \
GitHub var - [atl-var.sh](vm%2Fansible%2Fstack%2Fatl-var.sh)
 ```shell
 atlantis server \
 --atlantis-url="$URL" \
 --gh-user="$USERNAME" \
 --gh-token="$TOKEN" \
 --gh-webhook-secret="$SECRET" \
 --repo-allowlist="$REPO_ALLOWLIST"
 ```
3. Потребуется GH token и secret..
- Gh токен генерим с кабинета
- секрет для хука `echo $RANDOM | md5sum | head -c 20; echo;` копируем себе тк основная тема - чтоб потом совпал с двух сторон
4. Запускаем Docker - [Dockerfile](vm%2Fansible%2Fstack%2FDockerfile) \
плюс потребовались ключи `--default-tf-version` `--repo-allowlist`
```shell
sudo docker run -p 4141:4141 1nxs/atlantis-custom:2.5 server --config /tmp/server.yaml --repo-config /tmp/atlantis.yaml --default-tf-version 1.3.6
```
5. В качестве результата приложите ссылку на файлы [server.yaml](vm%2Fansible%2Fstack%2Fserver.yaml) и [atlantis.yaml](vm%2Fansible%2Fstack%2Fatlantis.yaml).
> все материалы по задаче собраны в каталог [stack](vm%2Fansible%2Fstack)

## Задача 3. Знакомство с каталогом модулей. 

1. В [каталоге модулей](https://registry.terraform.io/browse/modules) найдите официальный модуль от aws для создания
`ec2` инстансов. 
2. Изучите как устроен модуль. Задумайтесь, будете ли в своем проекте использовать этот модуль или непосредственно 
ресурс `aws_instance` без помощи модуля?
3. В рамках предпоследнего задания был создан ec2 при помощи ресурса `aws_instance`. 
Создайте аналогичный инстанс при помощи найденного модуля.   

В качестве результата задания приложите ссылку на созданный блок конфигураций. 

### Ответ
Для Yandex Cloud модулей у Terraform нет.
Доступа до AWS нет у меня, так что выкладка будет основываться на чтении кода *.tf
1. В [каталоге модулей](https://registry.terraform.io/browse/modules) найдите официальный модуль от aws для создания
`ec2` инстансов. 
> https://github.com/terraform-aws-modules/terraform-aws-ec2-instance

2. Изучите как устроен модуль. Задумайтесь, будете ли в своем проекте использовать этот модуль или непосредственно 
ресурс `aws_instance` без помощи модуля?
```terraform
module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "single-instance"

  ami                    = "ami-ebd02392"
  instance_type          = "t2.micro"
  key_name               = "user1"
  monitoring             = true
  vpc_security_group_ids = ["sg-12345678"]
  subnet_id              = "subnet-eddcdzz4"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```
По количеству кода - примерно одно и тоже. Для единичного проекта развертывания смысл в использовании модуля почти сводится к нулю. В случае создания\эксплуатации большой инфраструктуры - конечно использование оправдано, тк упрощает развертывание, уменьшает кол-во возможности хардкода, прощее вносить массовые изменения. \
Лично я - стал бы, тк следую логике что если где-то можно сделать возможность "динамического" - то лучше закладывать её сразу. 


3. В рамках предпоследнего задания был создан ec2 при помощи ресурса `aws_instance`. 
Создайте аналогичный инстанс при помощи найденного модуля.

Собственно, в рамках предпоследнего задания уже был `yandex_compute_instance` \
Немного фантазий, скорее всего придётся подправить еще.. но суть:
<details><summary>AWS main.tf</summary>

```terraform
provider "aws" {
  region = "eu-north-1"
}

module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "aws-74-lab"

  ami                    = "ami-ebd02392"
  instance_type          = "t3.micro"
  key_name               = "user1"
  vpc_security_group_ids = ["sg-12345678"]
  subnet_id              = "subnet-eddcdzz4"
 
  count = local.instance_count[terraform.workspace]
 
  tags = {
    Terraform   = "true"
    Name = "${terraform.workspace}-count-${count.index}"
    Name = "my-comp-${count.index}"
  }
  lifecycle {
    create_before_destroy = true
  }
}

```
</details>