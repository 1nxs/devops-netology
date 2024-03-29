# Домашнее задание к занятию "7.5. Основы golang"

С `golang` в рамках курса, мы будем работать не много, поэтому можно использовать любой IDE. 
Но рекомендуем ознакомиться с [GoLand](https://www.jetbrains.com/ru-ru/go/).  

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

### Ответ
"_Однако за время пути собака могла подрасти!_"
(С.Маршак ©)

Оффициальный сайт: https://go.dev \
Песочница https://go.dev/play/
```shell
❯ go version
go version go1.19.5 linux/amd64
```

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана. 
### Ответ

- [x] Done\
Интерактивная консоль теперь живёт тут: https://go.dev/tour

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
    Для взаимодействия с пользователем можно использовать функцию `Scanf`:
    ```
    package main
    
    import "fmt"
    
    func main() {
        fmt.Print("Enter a number: ")
        var input float64
        fmt.Scanf("%f", &input)
    
        output := input * 2
    
        fmt.Println(output)    
    }
    ```

1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```
1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

В виде решения ссылку на код или сам код. 

### Ответ
[ссылка на код](./src/task3.go)
<details><summary>Задача 3.1</summary>

```go
func task3_11() {
	fmt.Print("Input length in meters: ")
	var input float64
	fmt.Scanf("%f", &input)

	output := input / 0.3048

	fmt.Printf("%v meters is: %4.4f feet.\n", input, output)
}
```
</details>

<details><summary>Задача 3.2</summary>

```go
func task3_20() {
    // пример списка из задачи
	x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
	min := x[0]
	for _,y := range x {
		if y < min {
			min = y
		}
	}
	fmt.Println("Min integer is:",min)
}
```
</details>

<details><summary>Задача 3.3</summary>

```go
func task3_30() {
    for i := 1; i <= 101; i++ {
        if (i % 3) == 0 {
        fmt.Printf( "[%v] ", i )
        }
    }
}
```

</details>

---
**upd:** дорабатываем "Можно запросить исходные данные у пользователя"

<details><summary>Задача 3.3</summary>

```go
func task3_31() {
    fmt.Print("Enter min integer: ")
    var min int
    fmt.Scanf("%d", &min)

    fmt.Print("Enter max integer: ")
    var max int
    fmt.Scanf("%d", &max)

    for i := min; i <= max; i++ {
        if (i % 3) == 0 {
        fmt.Printf( "[%v] ", i )
        }
    }
}
```

</details>

---

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания.


