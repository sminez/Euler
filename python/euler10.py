#! /usr/bin/ python3.4
'''Find the sum of the primes below n.'''
import time
from euler import e_sieve

def euler10():
    n = int(input('Please specify an upper bound:\n'))
    start = time.time()
    primes = e_sieve(n, False)
    psum = sum(primes)
    print('The primes below {0} are:\n{1}'.format(n, primes))
    print('\n--> The sum of the primes below {0} is {1}'.format(n, psum))
    finish = time.time() - start
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")


if __name__=='__main__':
    euler10()
