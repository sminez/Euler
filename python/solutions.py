'''
Solutions to the Project Euler Problems
```````````````````````````````````````
'''
from euler_lib import *


###############################################################################
# Values required for the problems as specified #
#################################################
BIG_INT_PROBLEM_8 = (
"7316717653133062491922511967442657474235534919493496983520312774"
"506326239578318016984801869478851843858615607891129494954595017379583"
"319528532088055111254069874715852386305071569329096329522744304355766"
"896648950445244523161731856403098711121722383113622298934233803081353"
"362766142828064444866452387493035890729629049156044077239071381051585"
"930796086670172427121883998797908792274921901699720888093776657273330"
"010533678812202354218097512545405947522435258490771167055601360483958"
"644670632441572215539753697817977846174064955149290862569321978468622"
"482839722413756570560574902614079729686524145351004748216637048440319"
"989000889524345065854122758866688116427171479924442928230863465674813"
"919123162824586178664583591245665294765456828489128831426076900422421"
"902267105562632111110937054421750694165896040807198403850962455444362"
"981230987879927244284909188845801561660979191338754992005240636899125"
"607176060588611646710940507754100225698315520005593572972571636269561"
"882670428252483600823257530420752963450")

###############################################################################


@timed
def euler1(a, b, u_bound):
    '''
    Find the sum of the multiples of m and n below upper bound
    '''
    def asum(ad, u_bound):
        n = (u_bound - 1) // ad
        return (n / 2) * (n + 1) * ad
    s = asum(a, u_bound) + asum(b, u_bound) - asum(a*b, u_bound)
    return int(s)


@timed
def euler2(n):
    '''
    Find the sum of even valued Fibonacci numbers below n
    '''
    fib_sum = 0
    fibs = lazy_fibs()
    next_fib = next(fibs)
    while next_fib < n:
        if next_fib % 2 == 0:
            fib_sum += next_fib
        next_fib = next(fibs)
    return fib_sum


@timed
def euler3(n):
    '''
    Finding the prime factors of an int is used enough that this is a
    library function in euler_lib.
    '''
    return p_factors(n)


@timed
def euler4(n):
    '''
    Find the largest palendromic product of two n-digit numbers
    '''
    upper = 10 ** n
    lower = 10 ** (n - 1)
    step_size = min(1000, int(upper * 0.1))
    amax = bmax = upper
    amin = bmin = upper - step_size
    stepped = False

    while True:
        prods = ((a * b, a, b) for a in range(amin, amax) for b in range(bmin, bmax))
        palenprods = [p for p in prods if str(p[0]) == str(p[0])[::-1]]
        if palenprods:
            return max(palenprods)
        else:
            amin = amin if stepped else bmin
            bmax = amin if stepped else bmax
            bmin = bmin - step_size if stepped else bmin
            stepped = not stepped
            if bmin < lower:
                # No solution in the required range
                return None


@timed
def euler5(n):
    '''
    Find the smallest number that can be divided evenly by 1..n
    '''
    factmap = dict()
    for i in range(1, n+1):
        factors = p_factors(i)
        for f in factors:
            freq = factors.count(f)
            previous = factmap.setdefault(f, 0)
            factmap[f] = freq if freq > previous else previous
    smallest = 1
    for factor, count in factmap.items():
        smallest *= factor ** count
    return smallest


@timed
def euler6(n):
    '''
    Find the difference between the square of sums and sum of squares
    of the integers 1 to n
    '''
    square_sum = sum(range(1, n+1)) ** 2
    sum_square = 0
    for i in range(1, n+1):
        sum_square += i ** 2
    return square_sum - sum_square


@timed
def euler7(n):
    '''Return the nth prime number'''
    return nth(n, lazy_primes())


@timed
def euler8(l, n=None):
    '''Find the largest product of l consecutive digits in n'''
    if n:
        n = str(n)
    else:
        n = BIG_INT_PROBLEM_8

    # Any product containing 0 is 0 so this partitions our input
    split_on_zero = n.split("0")
    largest = 0
    for fragment in split_on_zero:
        if len(fragment) > l:
            over_l = len(fragment) - l
            for offset in range(over_l + 1):
                product = 1
                for index in range(l):
                    product *= int(fragment[index + offset])
                largest = max(product, largest)
    return largest


@timed
def euler9(target):
    '''
    Find a Pythagorean triple that sums to the given target and return
    its product.
    '''
    def trip(c):
        c2 = c ** 2
        for a in range(1, c):
            b = (c2 - a ** 2) ** 0.5
            if b.is_integer():
                return (a, int(b), c)
        return ()

    # smallest hypotenuse for a triple is 5
    for hypot in range(5, target):
        t = trip(hypot)
        if t:
            # see if a+b+c is a factor of the target
            quot = target / sum(t)
            if quot.is_integer():
                # the quotient is an int then we have our answer
                a, b, c = solution = tuple(map((lambda n: int(quot * n)), t))
                return (solution, a * b * c)
    else:
        # Failed to find a solution
        return None


@timed
def euler10(n):
    '''
    Find the sum of the primes below n
    '''
    return sum(primes_to_n(n))
