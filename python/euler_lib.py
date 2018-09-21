'''
Base clases and helpers for the Project Euler problems.
-------------------------------------------------------
Everything is implemented as a generator where a collection
data type would be returned and the solutions themselves
handle conversion to concrete data structures.

In addition, I have tried to keep everything purely functional
wherever possible.
'''
from math import factorial
import itertools as itools
import functools as ftools
import operator as op
import random
import time


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
def euler_solution(func):
    '''
    Time the execution of a function and print its result.
    '''
    def wrapped(*args, **kwargs):
        print(func.__doc__)
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
        return
    else:
        while True:
            yield (elem for elem in current_slice)

            try:
                next_element = next(remaining)
            except StopIteration:
                return

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
        k += 1


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


def probably_prime(n, k=20):
    """
    Check n for primalty using the Miller-Rabin method
        https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
        http://mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html

    Return True if n passes k rounds of the Miller-Rabin primality test (and is
    probably prime). Return False if n is proved to be composite.

    NOTE: This is faster than generating primes >= n and checking if we are in
          the list but it is slower at generating a list of primes than
          using `lazy_primes`.
    """
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    # Handle simple known cases
    if n < 2:
        return False

    # Quick & small prime sieve for known small primes
    for p in small_primes:
        if n < p * p:
            return True

        if n % p == 0:
            return False

    # Not sieved by the small primes so run Miller-Rabin

    # Determine the values of r and s such that n == (2^r)s + 1
    r, s = 0, n - 1

    while s % 2 == 0:
        r += 1
        s //= 2

    # Run our k iterations of the algorithm in different bases:
    #   If a^s == 1 (mod n)
    #   or a^2js == -1 (mod n) for some j, 0 <= j <= r-1
    #   then n passes the test in base a.
    #   A prime will pass in all bases. If the smallest known composite that
    #   passes for a given base is known, then this can be used as a proof of
    #   primality for all primes below that bound.
    #   Using multiple tests of the first 7 primes are valid for every number
    #   up to 3.4x10^14.
    for _ in range(k):
        # Select a base
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)  # a^s (mod n)

        if x == 1 or x == n - 1:
            # We passed the first test in this base so don't bother
            # with the second one.
            continue

        # Check for a passing value of j via repeated squaring. When we
        # reach this point, x is already a^s (mod n).
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # Failed both tests so this is a composite
            return False

    # Passed both so this is _probably_ prime (known prime if we are below
    # the threshold)
    return True


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


def largest_power_of_2(n):
    '''Find the largest power of 2 less than n along with the power'''
    res, power = 2, 1
    while res <= n:
        power += 1
        res *= 2
    return res // 2


def powers_of_2(n):
    '''Find all powers of 2 less than n and their power'''
    res, power = 2, 1
    powers = {2: 1}
    while True:
        power += 1
        res *= 2
        if res <= n:
            powers[res] = power
        else:
            break
    return powers


def nCr(n, r):
    '''
    Compute n chose r using binomial coefficients
    '''
    return factorial(n) / (factorial(r) * factorial(n - r))


def spiral_corners():
    '''
    Yield the corners of a number spiral in layers. Each layer
    after the first contains 4 corners.
    '''
    n, step = 1, 1

    yield [n]

    while True:
        layer = []

        for i in range(4):
            n += step * 2
            layer.append(n)

        yield layer

        # New layer so increase the step size
        step += 1
