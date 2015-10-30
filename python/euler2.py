#! /usr/bin/python3.4
"""Find the sum of the even valued terms of the Fibonacci sequence that do not exceed a given upper bound."""

from euler import fibonacci
import time


def euler2():
    print("This program will find the sum of the even valued terms of the Fibonacci sequence that do not exceed a given upper bound.")
    upper_bound = int(input("Please select an upper bound to calculate values to::\n"))
    start = time.time()
    fib = fibonacci(upper_bound)
    # -- Selecting even valued terms and finding their sum
    fib_sum = 0
    for x in fib:
        if x % 2 == 0:
            fib_sum += x
    finish = (time.time() - start)
    print("\n>>>The sum of the even valued terms is:: %d\n\n" % (fib_sum))
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler2()
