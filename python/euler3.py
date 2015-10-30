#! /usr/bin/env python3.4
"""Find the largest prime factor for a given number."""

from euler import e_sieve, factorise
import time


def euler3():
    global user_number
    user_number = int(input("\nPlease specify a number to factorise...\n\n"))

    start = time.time()
    prime_list = e_sieve(user_number, True)
    factors = factorise(user_number, prime_list)
    if 1 in factors:
        factors.remove(1)
    print("\nThe prime factors of %d are %s.\n" % (user_number, factors))
    finish = (time.time() - start)
    if len(factors) == 1:
        print(">>You have entered a prime number! Its greatest factor is itself!\n\n")
    elif len(factors) > 0:
        max_factor = max(factors)
        print(">>The greatest prime factor of %d is %d.\n\n" % (user_number, max_factor))
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler3()
