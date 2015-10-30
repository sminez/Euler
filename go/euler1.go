// Find the sum of all the multiples of 3 or 5 below 1000.
package main

import "fmt"

func multiple_sum(base, upper_bound int) int {
	var total int = 0
	roof := int(upper_bound / base)
	fmt.Printf("\n    There are %d %ds below %d", roof, base, (upper_bound + 1))
	for i := 0; i < roof; i++ {
		total += base * (int(i) + 1.0)
	}
	fmt.Printf("\n    The sum of the multiples of %d = %d", base, total)
	return total
}

func aSum(A, D, N int) int {
	/*	Floats cause problems!!!
		-> need to use float64 for precision but there is no
		warning of overflow unless I manually check!
		Also, setting the upper bound too high makes the result negative...
		-> Probably a two's compliment problem? */
	a := float64(A)
	d := float64(D)
	n := float64(N)
	Sn := int(n * (2.0*a + (n-1.0)*d) / 2.0)
	return int(Sn)
}

func main() {
	fmt.Println("This program will calculate the sum of the multiples of two specified integers below a given value.")
	var (
		mult1       int
		mult2       int
		upper_bound int
	)
	fmt.Println("What is the first integer you want to use?")
	fmt.Scanf("%d", &mult1)
	fmt.Println("What is the second integer you want to use?")
	fmt.Scanf("%d", &mult2)
	overlap := mult1 * mult2
	fmt.Println("Please specify an upper bound for the calculation:")
	fmt.Scanf("%d", &upper_bound)
	fmt.Printf("\n  Calculating the sum of the multiples of %d and %d below %d", mult1, mult2, upper_bound)
	upper_bound -= 1

	fmt.Println("\n--> Take 1: using a for loop to sum up required values and subtract the overlap:")
	grand_total := multiple_sum(mult1, upper_bound) + multiple_sum(mult2, upper_bound) - multiple_sum(overlap, upper_bound)
	fmt.Println("\n\nThe grand total is: ", grand_total)

	fmt.Println("\n--> Take 2: using the sun of an arithmetic series:")
	n1 := upper_bound / mult1
	n2 := upper_bound / mult2
	n3 := upper_bound / (mult1 * mult2)
	S1 := aSum(mult1, mult1, n1)
	S2 := aSum(mult2, mult2, n2)
	S3 := aSum(overlap, overlap, n3)
	fmt.Println(mult1, n1, S1)
	fmt.Println(mult2, n2, S2)
	fmt.Println(overlap, n3, S3)
	total := S1 + S2 - S3
	fmt.Println("\n\nThe grand total is: ", total)
}
