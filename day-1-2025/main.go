package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type Rotation struct {
	direction int
	amount    int
}

func mod(a int, b int) int {
	return (a%b + b) % b
}

func readFileAsString(filePath string) ([]string, error) {
	file, err := os.Open(filePath)

	if err != nil {
		return nil, err
	}

	lines := []string{}
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	return lines, nil
}

func inputToRotations(rotaionStrings []string) []Rotation {
	result := []Rotation{}
	for _, line := range rotaionStrings {
		amount, _ := strconv.Atoi(strings.TrimSpace(line[1:]))
		direction := -1
		if line[0] == 'R' {
			direction = 1
		}
		result = append(result, Rotation{
			direction: direction,
			amount:    amount,
		})
	}
	return result
}

func solvePartOne(rotations []Rotation) int {
	countTo0 := 0
	currentValue := 50
	for _, rotation := range rotations {
		currentValue += rotation.amount * rotation.direction
		currentValue = mod(currentValue, 100)
		if currentValue == 0 {
			countTo0 += 1
		}
	}
	return countTo0
}

func solvePartTwo(rotations []Rotation) int {
	countTo0 := 0
	currentValue := 50
	for _, rotation := range rotations {
		if rotation.direction == 1 {
			countTo0 += (currentValue + rotation.amount) / 100
			currentValue = mod(currentValue+rotation.amount, 100)
		} else {
			flipped_dir := mod(100-currentValue, 100)
			countTo0 += (flipped_dir + rotation.amount) / 100
			currentValue = mod(currentValue-rotation.amount, 100)
		}
	}
	return countTo0
}

const IN_FILE_PATH = "./input.txt"

func main() {
	data, err := readFileAsString(IN_FILE_PATH)

	if err != nil {
		println(err)
		panic("Error reading from " + IN_FILE_PATH)
	}

	if len(os.Args) != 2 {
		panic("Exactly one arg is expected")
	}
	arg := os.Args[1]

	if arg != "1" && arg != "2" {
		panic("Arg can only be 1 or 2 for part 1 ore part 2 of the problem respectively")
	}

	rotations := inputToRotations(data)

	if arg == "1" {
		println(solvePartOne(rotations))
	} else {
		println(solvePartTwo(rotations))
	}
}
