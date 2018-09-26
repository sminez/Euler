package euler

import java.util.Random
import kotlin.math.pow
import kotlin.coroutines.experimental.*


/**
Check n for primalty using the Miller-Rabin method
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    http://mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html

Return True if n passes k rounds of the Miller-Rabin primality test (and is
probably prime). Return False if n is proved to be composite.

NOTE: This is faster than generating primes >= n and checking if we are in
      the list but it is slower at generating a list of primes than
      using `lazy_primes`.
**/
fun probablyPrime(n: Int, k: Int = 20): Boolean {
    val smallPrimes = listOf(2, 3, 5, 7, 11, 13, 17, 23, 29, 31)

    // Handle small known cases quickly
    if (n < 2) return false

    for (p in smallPrimes) {
        if (n < p * p) return true
        if (n % p == 0) return false
    }

    var r = 0
    var s = n - 1
    val uBound = n - 1

    while (s % 2 == 0) {
        r += 1
        s /= 2
    }

    for (i in 1..k) {
        val a = Random().nextInt(uBound - 2) + 2
        var x = a.toDouble().pow(s).toInt() % n

        if (x == 1 || x == uBound) {
            continue
        }

        var flag = false

        for (j in 0..r-1) {
            x = x.toDouble().pow(2).toInt() % n
            if (x == uBound) {
                flag = true
                break
            }
        }
        // If we didn't break then we are composite
        if (flag == false) return false

    }
    return true
}


fun primes() = buildSequence {
    var sieve = HashMap<Int, MutableList<Int>>()
    var k: Int = 2

    while (true) {
        var kFactors = sieve.get(k)

        if (kFactors != null) {
            sieve.remove(k)
            for (f in kFactors) {
                var facts = sieve.getOrDefault(f+k, mutableListOf<Int>())
                facts.add(f)
                sieve.put(f+k, facts)
            }
        } else {
            yield(k)
            sieve.put(k*k, mutableListOf(k))
        }
        k += 1
    }
}


fun primesToN(n: Int): List<Int> {
    return primes().takeWhile({it < n}).toList()
}


fun pFactors(n: Int): List<Int> {
    var factors = mutableListOf<Int>()
    for (p in primesToN(Math.sqrt(n as Double) as Int + 1)) {
        while (n as Int % p == 0 as Int) {
            factors.add(p)
            var x = n as Int
            x /= p
        }
    }

    if (n != 1 as Int) {
        factors.add(n)
    }
    return factors
}
