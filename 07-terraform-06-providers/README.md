# Домашнее задание к занятию "7.6. Написание собственных провайдеров для Terraform."

Бывает, что 
* общедоступная документация по терраформ ресурсам не всегда достоверна,
* в документации не хватает каких-нибудь правил валидации или неточно описаны параметры,
* понадобиться использовать провайдер без официальной документации,
* может возникнуть необходимость написать свой провайдер для системы используемой в ваших проектах.   

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[https://github.com/hashicorp/terraform-provider-aws.git](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  


1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.   
1. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
 * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.
 * Какая максимальная длина имени? 
 * Какому регулярному выражению должно подчиняться имя? 
    
### Ответ
1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.   
 - `ResourcesMap` -> `/internal/provider/provider.go` - [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/provider/provider.go#L944)
 - `DataSourcesMap` -> `/internal/provider/provider.go`- [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/provider/provider.go#L419)
2. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
   * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.
     - `/internal/service/sqs/queue.go` - [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/service/sqs/queue.go)
     - Конфликтует `name` с `name_prefix` - [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/service/sqs/queue.go#L83)
     - <details><summary>code</summary>

       ```go
        "name": {
            Type:          schema.TypeString,
            Optional:      true,
            Computed:      true,
            ForceNew:      true,
            ConflictsWith: []string{"name_prefix"},
        },
        "name_prefix": {
            Type:          schema.TypeString,
            Optional:      true,
            Computed:      true,
            ForceNew:      true,
            ConflictsWith: []string{"name"},
        },
        ```
      </details>       

   * Какая максимальная длина имени? 
     - `/internal/service/sqs/queue.go` - [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/service/sqs/queue.go)
     - Функция `resourceQueueCustomizeDiff` - [permalink](https://github.com/hashicorp/terraform-provider-aws/blob/1092267d84a47daadc69dadba6c5404cb4b173ce/internal/service/sqs/queue.go#L414)
     - [code](src%2FresourceQueueCustomizeDiff.go)
     - максимальная длина имени `80`
     - в случае с FIFO очередью -  основная часть имени `75`, тк в конце должно прибавляться `.fifo` - что даёт `+5` символов = `80`
   * Какому регулярному выражению должно подчиняться имя?
     - `^[a-zA-Z0-9_-]{1,80}$` - Имя может содержать буквы, цифры, дефис, подчеркивания, точки. Дллина от 1 до 80 символов.
     - `^[a-zA-Z0-9_-]{1,75}\.fifo$` - для FIFO. Имя может содержать буквы, цифры, дефис, подчеркивания, точки. Длина от 1 до 75 символов. После имени должно быть `.fifo`



<details><summary>Оффтоп</summary>
Пока искал это всё - посмотрел как пишутся тесты, теперь можно поглядеть на пердыдущую задачу еще чуть интереснее..
</details>

## Задача 2. (Не обязательно) 
В рамках вебинара и презентации мы разобрали как создать свой собственный провайдер на примере кофемашины. 
Также вот официальная документация о создании провайдера: 
[https://learn.hashicorp.com/collections/terraform/providers](https://learn.hashicorp.com/collections/terraform/providers).

1. Проделайте все шаги создания провайдера.
2. В виде результата приложение ссылку на исходный код.
3. Попробуйте скомпилировать провайдер, если получится то приложите снимок экрана с командой и результатом компиляции.   

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
