'''
Base clases and helpers for the Project Euler problems.
-------------------------------------------------------
Everything is implemented as a generator where a collection
data type would be returned and the solutions themselves
handle conversion to concrete data structures.

In addition, I have tried to keep everything purely functional
wherever possible.
'''
from types import GeneratorType
import itertools as itools
import functools as ftools
import operator as op
import time

from fmap import fmap


#############################################################
# Make some library functions available without namespacing #
#############################################################
takewhile = itools.takewhile
dropwhile = itools.dropwhile
groupby = itools.groupby
reduce = ftools.reduce


#############################################################
# Helpers for analysing the solutions themselves            #
#############################################################
def timed(func):
    '''
    Time the execution of a function and print its result.
    '''
    def wrapped(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        print('Execution took {0:.7f} seconds'.format(time.time() - s))
        print(res)
    return wrapped


###################################################
# General purpose helpers for use with generators #
###################################################
def take(n, col):
    '''
    Return the up to the first n items from a generator
    '''
    return (next(col) for k in range(n))


def drop(n, col):
    '''
    Drop the first n items from a generator and then return the rest
    '''
    # Take and discard the first n values
    for k in range(n):
        try:
            next(col)
        except StopIteration:
            return col
    return col


def nth(n, col):
    '''
    Return the nth element of a generator
    '''
    for k in range(n):
        try:
            element = next(col)
        except StopIteration:
            raise IndexError
    return element


# NOTE: This is just an alias for reduce with a reordered signature
# Python's reduce is reduce(func, col, acc) which looks wrong to me...!
def foldl(func, acc=None, col=[]):
    '''
    Fold a list into a single value using a binary function.
    '''
    return reduce(func, col, acc)


def scanl(func=op.add, acc=0, col=[]):
    '''
    Fold a collection from the left using a binary function
    and an accumulator into a list of values: [x, f(x), f(f(x), ...]
    '''
    with_acc = itools.chain([acc], col)
    return itools.accumulate(with_acc, func)



def flatten(lst):
    '''
    Flatten an arbitrarily nested list of lists into a single stream
    '''
    _list = ([x] if not isinstance(x, list) else flatten(x) for x in lst)
    return (element for element in sum(_list, []))


def windowed(size, col):
    '''
    Yield a sliding series of iterables of length _size_ from a collection.

    NOTE:
    - If the collection is a generator it will be drained by this
    - yields [] if the supplied collection has less than _size_ elements
    - keeps _size_ elements in memory at all times
    '''
    remaining = iter(col)
    current_slice = list(take(size, remaining))

    if len(current_slice) < size:
        raise StopIteration
    else:
        while True:
            yield (elem for elem in current_slice)
            next_element = next(remaining)
            if next_element:
                # Slide the window
                current_slice = current_slice[1:] + [next_element]
            else:
                # We've reached the end so return
                break


def l_windowed(size, col):
    '''
    A version of windowed that yields lists rather than generators
    '''
    for w in windowed(size, col):
        yield [elem for elem in w]


###################################################
# Mathematical sequences and functions            #
###################################################
def a_sum(a, n, d):
    '''
    Find the arithmetic sum of a series
    '''
    return int((n / 2) * (2 * a * (n - 1) * d))


def lazy_fibs():
    '''
    Infinite Fibonacci generator
    '''
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def lazy_primes():
    '''
    An infinite generator of primes based on a sieve that stores each prime
    indexed against its current greatest multiple.
    '''
    sieve = {}
    k = 2
    while True:
        # k_factors is a list of prime factors
        # (not guaranteed to be all of the prime factors of k)
        k_factors = sieve.get(k)
        if k_factors:
            # k is the current highest multiple of at least one prime
            # stored in the sieve. Delete it from the sieve and move its
            # prime factors to their next multiple.
            del sieve[k]
            for f in k_factors:
                sieve.setdefault(f + k, []).append(f)
        else:
            # k is a prime so return it and mark its square in the sieve
            # as the starting point for later filtering.
            # - This is valid for all primes p as all multiples of p
            #   below p^2 will be a composite pq where q is a prime
            #   or composite less than p.
            yield k
            sieve[k ** 2] = [k]
        k +=1


def primes_to_n(n):
    '''
    All primes below n
    '''
    primes = lazy_primes()
    p = next(primes)

    while p < n:
        yield p
        p = next(primes)


def p_factors(n):
    '''
    Find the prime factors of a number
    '''
    # Only need the primes up to sqrt(n) for factorisation.
    factors = []
    for p in primes_to_n(int(n ** 0.5) + 1):
        while n % p == 0:
            factors.append(p)
            n /= p
    # The final factor may be above sqrt(n) so we need to add it back
    # Or, n is evenly divided by the factors so far so ignore '1'.
    if n != 1:
        factors.append(int(n))
    return factors


def n_digit_pals(n):
    '''
    Find all n-digit palindromes
    '''
    def no_leading_0(n):
        '''Check if a stringified number has a leading zero'''
        return n[0] != '0'

    digits = [str(n) for n in range(9, -1, -1)]
    if n == 1:
        for k in range(9, -1, -1):
            yield k
    elif n == 2:
        for k in range(99, 0, -11):
            yield k
    else:
        pals = (k + str(m) + k for k in digits for m in n_digit_pals(n - 2))
        for k in map(int, filter(no_leading_0, pals)):
            yield k

