'''
Solutions to the Project Euler Problems
```````````````````````````````````````
'''
from collections import defaultdict, namedtuple
from itertools import combinations, groupby

from euler_lib import *
from euler_lib import euler_solution


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
    "882670428252483600823257530420752963450"
)

###############################################################################


@euler_solution
def euler1(a, b, u_bound):
    '''
    Find the sum of the multiples of m and n below upper bound
    '''
    def asum(ad, u_bound):
        n = (u_bound - 1) // ad
        return (n / 2) * (n + 1) * ad
    s = asum(a, u_bound) + asum(b, u_bound) - asum(a*b, u_bound)
    return int(s)


@euler_solution
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


@euler_solution
def euler3(n):
    '''
    Finding the prime factors of an int is used enough that this is a
    library function in euler_lib.
    '''
    return p_factors(n)


@euler_solution
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


@euler_solution
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


@euler_solution
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


@euler_solution
def euler7(n):
    '''Return the nth prime number'''
    return nth(n, lazy_primes())


@euler_solution
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


@euler_solution
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


@euler_solution
def euler10(n):
    '''
    Find the sum of the primes below n
    '''
    return sum(primes_to_n(n))


def euler11(matrix):
    '''
    Find the largest product in a grid
    '''
    pass


@euler_solution
def euler12(divisors=500):
    '''
    Find the first triangular to have more than a target number of divisors
    '''
    pass


@euler_solution
def euler13(str_ns):
    '''
    Work out the first 10 digits of the sum of 100 50-digit numbers
    '''
    pass


@euler_solution
def euler14(upper_bound=int(1e6)):
    '''
    Find the longest Collatz sequence with a starting number under
    `upper_bound`. Terms _can_ exceed this once the sequence starts.
    n -> n/2    (if n is even)
    n -> 3n + 1 (if n is odd)
    '''
    def step_forward(n):
        '''Continue the chain'''
        if n % 2 == 0:
            return n // 2
        else:
            return (3 * n) + 1

    n_to_len = {2: 2, 1: 1}

    for num in range(3, upper_bound+1):
        if n_to_len.get(num):
            continue  # Filled in already

        existing_chain = n_to_len.get(step_forward(num))
        if existing_chain:
            n_to_len[num] = existing_chain + 1
        else:
            chain = [num]
            next_num = step_forward(num)
            while next_num != 4:
                chain.append(next_num)
                next_num = step_forward(next_num)
            for i, n in enumerate(reversed(chain)):
                # 4 has a chain length of 3, Python indexing from 0
                n_to_len[n] = i + 4

    valid = ((k, v) for k, v in n_to_len.items() if k <= upper_bound)
    return sorted(valid, key=lambda x: x[1], reverse=True)


@euler_solution
def euler15(grid_size=20):
    '''
    Starting in the top left corner of a 2×2 grid, and only being able to move
    to the right and down, there are exactly 6 routes to the bottom right
    corner.
    How many such routes are there through a 20×20 grid?
    '''
    # This is simply Pascal's triangle and looking for the middle entry in the
    # 2 x grid_size row
    return int(nCr(grid_size * 2, grid_size))


@euler_solution
def euler16(power=1000):
    '''
    2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
    What is the sum of the digits of the number 2^1000?
    '''
    # Looks like there's no cool number theory solution, just brute force...
    return sum(map(int, str(2**power)))


@euler_solution
def euler27(bound=1000):
    '''
    Considering quadratics of the form:

        n^2+an+b,    where |a|<1000 and |b|≤1000

    where |n| is the modulus/absolute value of n
    e.g. |11|=11 and |−4|=4

    Find the product of the coefficients, a and b, for the quadratic expression
    that produces the maximum number of primes for consecutive values of n,
    starting with n=0.
    '''
    def _quad(a, b):
        def q(n):
            return n**2 + a * n + b
        return q

    prime_gen = lazy_primes()
    primes = [next(prime_gen)]

    def is_prime(n):
        while primes[-1] < n:
            primes.append(next(prime_gen))

        return n in primes

    best = None
    best_run = []

    # Starting at n=0 means that b must be prime so that cuts down
    # the range of coefficients we need to look at.
    for a in range(bound):
        for b in primes_to_n(bound+1):
            # We can have +ve and -ve coefficients
            for a_sign in [1, -1]:
                for b_sign in [1, -1]:
                    A = a * a_sign
                    B = b * b_sign
                    func = _quad(A, B)

                    n = 0
                    k = func(n)
                    run = []

                    while is_prime(k):
                        run.append(k)
                        n += 1
                        k = func(n)

                    if len(run) > len(best_run):
                        best_run = run
                        best = (A, B)
                        print(
                            f'Best so far: {best} -> {n+1} primes\n{best_run}'
                        )

@euler_solution
def euler28(width=5):
    def ring_total(r):
        return 16 * r**2 + 4 * r + 4

    n_rings = int((width - 1) / 2)

    total = 1  # centre

    for ring in range(n_rings):
        total += ring_total(ring+1)

    return total


@euler_solution
def euler35(bound=100):
    '''
    The number, 197, is called a circular prime because all rotations of the
    digits: 197, 971, and 719, are themselves prime.
    There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37,
    71, 73, 79, and 97.
    How many circular primes are there below one million?
    '''
    def rotations(n):
        '''Return ONLY the rotations, not the original number'''
        digits = [d for d in str(n)]
        rots = []
        for ix in range(1, len(digits)):
            rots.append(int(''.join(digits[ix:] + digits[:ix])))
        return rots

    candidates = set(primes_to_n(bound))
    circular_primes = []

    for c in candidates:
        if c > 10:
            # quickly exclude numbers we know won't work: primes > 10 must end
            # in 1, 3, 7 or 9 so only numbers comprising of those digits are
            # candidates.
            digits = map(int, str(c))
            if not all(d in [1, 3, 7, 9] for d in digits):
                continue

        if set(rotations(c)).issubset(candidates):
            circular_primes.append(c)

    return circular_primes


@euler_solution
def euler49():
    '''
    The arithmetic sequence, 1487, 4817, 8147, in which each of the terms
    increases by 3330, is unusual in two ways:
      (i) each of the three terms are prime
      (ii) each of the 4-digit numbers are permutations of one another.
    There are no arithmetic sequences made up of three 1-, 2-, or 3-digit
    primes, exhibiting this property, but there is one other 4-digit increasing
    sequence.
    What 12-digit number do you form by concatenating the three terms in this
    sequence?
    '''
    primes = primes_to_n(10000)

    # partition by containing digits
    groups = defaultdict(list)

    for p in primes:
        if p > 1000:
            key = frozenset(str(p))
            groups[key].append(p)

    # Keep those that have at least 3 values
    candidates = filter(lambda l: len(l) >= 3, groups.values())

    # Keep those with a consistant jump
    consistant = []
    for c in candidates:
        for a, b, c in combinations(c, 3):
            if b - a == c - b:
                consistant.append([a, b, c])

    return consistant


@euler_solution
def euler54(fname='data/poker.txt'):
    '''
    In the card game poker, a hand consists of five cards and are ranked, from
    lowest to highest, in the following way:

        High Card: Highest value card.
        One Pair: Two cards of the same value.
        Two Pairs: Two different pairs.
        Three of a Kind: Three cards of the same value.
        Straight: All cards are consecutive values.
        Flush: All cards of the same suit.
        Full House: Three of a kind and a pair.
        Four of a Kind: Four cards of the same value.
        Straight Flush: All cards are consecutive values of same suit.
        Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

    The cards are valued in the order:
    2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

    If two players have the same ranked hands then the rank made up of the
    highest value wins; for example, a pair of eights beats a pair of fives
    (see example 1 below). But if two ranks tie, for example, both players have
    a pair of queens, then highest cards in each hand are compared (see example
    4 below); if the highest cards tie then the next highest cards are
    compared, and so on.

    The file, poker.txt, contains one-thousand random hands dealt to two
    players. Each line of the file contains ten cards (separated by a single
    space): the first five are Player 1's cards and the last five are Player
    2's cards. You can assume that all hands are valid (no invalid characters
    or repeated cards), each player's hand is in no specific order, and in each
    hand there is a clear winner.

    How many hands does Player 1 win?
    '''
    card = namedtuple('card', 'val suit')
    val_rank = [
        '2', '3', '4', '5', '6',
        '7', '8', '9', 'T', 'J',
        'Q', 'K', 'A'
    ]
    suit_rank = ['D', 'C', 'H', 'S']

    def classify(hand):
        '''Determine the best hand from a set of 5 cards.'''
        hand = sorted(hand, key=lambda v: val_rank.index(v.val))
        vals = [c.val for c in hand]

        has_flush = len(set(c.suit for c in hand)) == 1
        ix = val_rank.index(hand[0].val)
        has_straight = vals == val_rank[ix:ix+5]
        akind = [list(g) for _, g in groupby(hand, key=lambda c: c.val)]
        akind = sorted(
            [a for a in akind if len(a) > 1],
            key=lambda a: len(a)
        )

        # Default to high card
        score = 1
        qualifier = val_rank.index(hand[-1].val)

        if has_straight and has_flush:
            if hand[0].val == 'T':
                # Royal Flush
                score = 10
                qualifier = suit_rank.index(hand[0].suit)
            else:
                # Straight flush
                score = 9

        elif len(akind) == 1:
            if len(akind[0]) == 4:
                # Four of a kind
                score = 8
            elif len(akind[0]) == 3:
                # Three of a kind
                score = 4
            elif len(akind[0]) == 2:
                # Pair
                score = 2

            qualifier = val_rank.index(akind[0][0].val)

        elif len(akind) == 2:
            if len(akind[1]) == 3:
                # Full house
                score = 7
            else:
                # Two pairs
                score = 3

            qualifier = (
                val_rank.index(akind[1][0].val),
                val_rank.index(akind[0][0].val)
            )

        elif has_straight:
            # Straight
            score = 5

        elif has_flush:
            # Flush
            score = 6

        return score, qualifier

    player_1_score = 0

    with open(fname, 'r') as f:
        for line in f:
            cards = [card(*c) for c in line.strip().split()]
            hand_1 = cards[:5]
            hand_2 = cards[5:]

            score_1, qual_1 = classify(hand_1)
            score_2, qual_2 = classify(hand_2)

            if score_1 > score_2:
                player_1_score += 1
            elif score_1 == score_2:
                if score_1 in [3, 7]:
                    # Two pairs or full house
                    q10, q11 = qual_1
                    q20, q21 = qual_2
                    if q10 > q20 or (q10 == q20 and q11 > q21):
                        player_1_score += 1
                else:
                    if qual_1 > qual_2:
                        player_1_score += 1

    return player_1_score
