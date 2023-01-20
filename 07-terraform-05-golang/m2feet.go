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

// Конвертер величины с записанным в код множителем
func task3_11() {
	fmt.Print("Input length in meters: ")
	var input float64
	fmt.Scanf("%f", &input)

	output := input / 0.3048

	fmt.Printf("%v meters is: %4.4f feet.\n", input, output)
}

func task3_20() {
// Помещаем строку из задачи 3_2
	x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
	min := x[0]
	for y := range x {
		if y < min {
			min = y
		}
	}
	fmt.Println("Min integer is: \n",min)
}

func main() {
    //task3_10()
    //task3_11()
    task3_20()

}