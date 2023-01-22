package main

import "fmt"


//Пример из задания
func task3_10() {
    fmt.Print("Enter a number: ")
    var input float64
    fmt.Scanf("%f", &input)
    output := input * 2
    fmt.Println(output)
}

// Задача 3_1
// Конвертер величины с записанным в код множителем
func task3_11() {
	fmt.Print("Input length in meters: ")
	var input float64
	fmt.Scanf("%f", &input)
	output := input / 0.3048
	fmt.Printf("%v meters is: %4.4f feet.\n", input, output)
}

// Задача 3_2
// Поиск наименьшего элемента в заданном списке
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

// Задача 3_3
// Вывод чисел от 1 до 100, которые делятся на 3
func task3_30() {
    for i := 1; i <= 101; i++ {
        if (i % 3) == 0 {
        fmt.Printf( "[%v] ", i )
        }
    }
}

func main() {
    //task3_10()
    //task3_11()
    //task3_20()
    task3_30()

}
