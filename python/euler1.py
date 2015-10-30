#! /usr/bin/python3.4
"""Find the sum of all the multiples of two integers below an upper bound. """

from euler import multiple_sum, arith_sum
import time


def euler1():
    print("\nThis program will calculate the sum of the multiples of two specified integers below a given value.")
    mult1 = int(input("\nWhat is the first integer you want to use?\n"))
    mult2 = int(input("\nWhat is the second integer you want to use?\n"))
    upper_bound = int(input("\nPlease specify an upper bound for the calculation:\n"))

    # -- This was the original version and it is FASTER than a list comp...
    print('--> Take 1: Original solution of multiple function calls and calculating THREE sums (m,n and overlap)...')
    s1 = time.time()
    overlap = mult1 * mult2
    upper_bound = upper_bound-1
    # corrects the upper bound so that the for loop will calculate BELOW that value rather than up to it
    grand_total = multiple_sum(mult1, upper_bound) + multiple_sum(mult2, upper_bound) - multiple_sum(overlap, upper_bound)
    f1 = time.time() - s1
    print(">>> The grand total is %d" % (grand_total))
    print("Solution found in " + str("{0:.5f}".format(f1)) + " seconds.\n")

    print('--> Take 2: Single for loop checking divison modulo m/n to add to a running total...')
    s2 = time.time()
    total = 0
    for n in range(1, upper_bound+1):
        if n % mult1 == 0 or n % mult2 == 0:
            total += n
    f2 = time.time() - s2
    print(">>> The grand total is %d" % (total))
    print("Solution found in " + str("{0:.5f}".format(f2)) + " seconds.\n")


    # -- This is a one liner but the list comp is SLOWER than the multiple function calls!
    print('--> Take 3: One liner with a list comprehension...')
    s3 = time.time()
    grand_total = sum([x for x in range(1, upper_bound+1) if x % mult1 == 0 or x % mult2 == 0])
    f3 = time.time() - s3
    print(">>> The grand total is %d" % (grand_total))
    print("Solution found in " + str("{0:.5f}".format(f3)) + " seconds.\n")


    print('--> Take 4: Using a formula for the sum of an arithmetic series...')
    s4 = time.time()
    n1 = upper_bound//mult1
    n2 = upper_bound//mult2
    n3 = upper_bound//overlap
    total = arith_sum(n1, mult1, mult1) + arith_sum(n2, mult2, mult2) - arith_sum(n3, overlap, overlap)
    f4 = time.time() - s4
    print(">>> The grand total is %d" % (total))
    print("Solution found in " + str("{0:.5f}".format(f4)) + " seconds.\n")


if __name__ == "__main__":
    euler1()
