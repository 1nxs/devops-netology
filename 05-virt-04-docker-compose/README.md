# Домашнее задание к занятию "4. Оркестрация группой Docker контейнеров на примере Docker Compose"

## Задача 1

Создать собственный образ операционной системы с помощью Packer.

Для получения зачета, вам необходимо предоставить:
- Скриншот страницы, как на слайде из презентации (слайд 37).

### Ответ
1. Слайда 37 не существует.
2. Предварительные танцы вокруг YC
<details>
Поставил себе zsh на хостмашину (Mint 21 Cinnamon)<br> 
Оставил пока на ней git ansible vagrant vbox<br>
docker + compose поднимаются внутри vbox, ибо нет уверенности, что далее "вот-это-всё" потребуется на хостмашине.

```shell
❯ yc init
❯ yc vpc network create --name vmdefnet --labels my-label=netology --description "Netology test net"
id: enp19a7vh----0d46n0k
folder_id: b1gprhi----91tp8b54f
created_at: "2022-11-14T19:22:30Z"
name: vmdefnet
description: Netology test net
labels:
  my-label: netology

❯ yc vpc subnet create --name vmsubnet-01 --zone ru-central1-a --range 10.87.0.0/24 --network-name=vmdefnet --description "Netology test subnet"
id: e9bf1unlvhc----kts6n6
folder_id: b1gprhi8----1tp8b54f
created_at: "2022-11-14T19:30:39Z"
name: vmsubnet-01
description: Netology test subnet
network_id: enp19a7vh----0d46n0k
zone_id: ru-central1-a
v4_cidr_blocks:
  - 10.87.0.0/24

```

</details>
3. Искомый скриншот

## Задача 2

Создать вашу первую виртуальную машину в Яндекс.Облаке.

Для получения зачета, вам необходимо предоставить:
- Скриншот страницы свойств созданной ВМ, как на примере ниже:

<p align="center">
  <img width="1200" height="600" src="./assets/yc_01.png">
</p>

## Задача 3

Создать ваш первый готовый к боевой эксплуатации компонент мониторинга, состоящий из стека микросервисов.

Для получения зачета, вам необходимо предоставить:
- Скриншот работающего веб-интерфейса Grafana с текущими метриками, как на примере ниже
<p align="center">
  <img width="1200" height="600" src="./assets/yc_02.png">
</p>

## Задача 4 (*)

Создать вторую ВМ и подключить её к мониторингу развёрнутому на первом сервере.

Для получения зачета, вам необходимо предоставить:
- Скриншот из Grafana, на котором будут отображаться метрики добавленного вами сервера.

