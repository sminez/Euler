/* By considering the terms of the fibonacci sequence
   that do not exceed 4 000 000, find the sum of the even terms
*/

package main

import "fmt"

func fib_list(upper int) int{

}

func main() {
	fib := fib_list(upper_bound)
    fib_sum := 0
    for i := 0; i < len(fib); i++ {
        if fib[i] % 2 == 0:
            fib_sum += fib[i]
    }
}

/*
PYTHON VERSION

def fibonacci(upper):
    fib_list = [1, 2]
    fib_next = 0
    fib1 = 1
    fib2 = 2
    print(fib_list)
    while fib1 + fib2 <= upper:
        fib_next = fib1 + fib2
        fib1 = fib2
        fib2 = fib_next
        fib_list.append(fib_next)
#NOTE:: .append() does not return anything! You just call it on a list and it will update it.
        print(fib_list)
    return fib_list


def euler2():
  print("This program will find the sum of the even valued terms of the Fibonacci sequence that do not exceed a given upper bound.")
  upper_bound = int(input("Please select an upper bound to calculate values to::\n"))
  start=time.time()
  fib = fibonacci(upper_bound)
  #selecting even valued terms and finding their sum
  fib_sum = 0
  for x in fib:
    if x % 2 == 0:
      fib_sum += x
  finish=(time.time()-start)
  print("\n>>>The sum of the even valued terms is:: %d\n\n" % (fib_sum))
  print("Solution found in", finish, "seconds.\n\n")

  */