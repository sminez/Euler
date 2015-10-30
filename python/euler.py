#! /usr/bin/env python3.4
##############################################################################################################################
""" Module containing all functions and classes developed as part of forming solutions to the projecteuler.net problems. """
##############################################################################################################################


def multiple_sum(n, upper_bound):
    total = 0
    roof_n = upper_bound//n
    # print("    There are %d %ds below %d" % (roof_n, n, (upper_bound + 1)))
    for x in range(roof_n):
        # NOTE the range(n) function will generate a list that is n elements in size, stating at 0
        total += n*(x + 1)
    # print("    The sum of the multiples of %d = %d" % (n, total))
    return total


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
        print(fib_list)
    return fib_list


# -- The root argument allows you to only return primes below the sqrt of number
def e_sieve(number, root):
    if root:
        number = int(number**0.5)
    primes = []
    # This next line will generate a list of number+1 elements all set to Boolean True.
    sieve = [True] * (number+1)

    # The following for loop will start at index 2 and add the index (2) to primes.
    # It will then mask out ALL multiples of 2 (second for loop).
    # After that it will only run the sieve if that element has not been set to false previously.
    for p in range(2, number+1):
        if sieve[p]:   # default test is against the argument being True.
            primes.append(p)
            for i in range(p*p, number+1, p):
                sieve[i] = False
    return primes


def factorise(number, divisors):
    original = int(number)
    factors = []

    for n in range(0, len(divisors)):
        while number % divisors[n] == 0:
            factors.append(divisors[n])
            number /= divisors[n]
    if number != 0:
        factors.append(int(number))
    if 1 in factors:
        factors.remove(1)
    return factors


def arith_sum(n, a, d):
    nsum = int((n/2)*(2*a+(n-1)*d))
    return nsum
