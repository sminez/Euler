#!/usr/bin/env python3.4
"""A palindromic number reads the same both ways. Find the largest palindrome made from the product of n-digits."""

import time


def euler4():
    print("A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.")
    n_digits = int(input("Please define the number of digits you would like to go up to::\n"))
    start = time.time()
    upper = 10 ** n_digits
    print(upper)
    candidates = [x * y for x in range(1, upper) for y in range(1, upper) if str(x * y) == str(x * y)[::-1]]
    print(candidates)
    max_candidate = max(candidates)
    finish = (time.time() - start)
    print("the largest palindromic product is %d" % max_candidate)
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler4()
