#!/usr/bin/env python3.4
"""Determine the nth prime number."""

"""
It might be fun to have this write to file with the following format:
    prime #n -> p
    time taken to find value
    average time per prime so far
"""
import time

def euler7():
    print("The first 6 prime numbers are:: 2, 3, 5, 7, 11 and 13.\n")
    target = int(input("Which prime number would you like to know?\n"))
    print("Calculating...\n")
    start = time.time()
    primecount = 1
    n = 1
    primes = [2]
    while primecount < target:
        n += 1
        for p in primes:
            if n % p == 0:
                break
            if p == primes[-1]:
                primes.append(n)
                primecount += 1
    finish = (time.time() - start)
    print(primes)
    print("Prime number " + str(target) + " is " + str(primes[-1]))
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")


if __name__ == "__main__":
    euler7()
