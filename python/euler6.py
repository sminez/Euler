#!/usr/bin/env python3.4
"""Find the difference between the sum of the squares and the square of the sums of the first n natural numbers."""

from euler import arith_sum
import time


def euler6():
    one_to_n = int(input("\n Please enter and upper bound:: \n"))
    start = time.time()
    sumsquares = 0
    for x in range(1, one_to_n + 1):
        sumsquares += x ** 2
    print("\n The sum of the squares of the numbers 1 to", one_to_n, "is", sumsquares)

    squaresum = (arith_sum(one_to_n, 1, 1)) ** 2
    print("\n The square of the sum of the numbers 1 to", one_to_n, "is", squaresum)

    difference = squaresum - sumsquares
    finish = (time.time() - start)
    print("\n The difference is", difference, "\n")
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler6()
