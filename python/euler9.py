#! /usr/bin/env python3.4
'''There exists exactly one Pythagorean triplet for which a + b + c = 1000. Find the product abc.'''

import time


def euler9():
    start = time.time()
    # -- this is brute force, slow and inelegant! Find a better way!!!
    magic_pyth = [(a,b,c) for a in range(1,500) for b in range(1,500) for c in range(1,500) if a<b<c and (a**2 + b**2) == c**2 and a+b+c == 1000]
    print(magic_pyth)
    a, b, c = magic_pyth[0]
    product = a*b*c
    print('The product is ' + str(product))
    finish = time.time() - start
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler9()
