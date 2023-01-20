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

//Конвертер величины с записанным в код множителем
func task3_11() {
	fmt.Print("Input length in meters: ")
	var input float64
	fmt.Scanf("%f", &input)

	output := input * 0.3048

	fmt.Printf("%v feet is: %v meters.\n", input, output)
}

func main() {
    //task3_10()
    task3_11()
}