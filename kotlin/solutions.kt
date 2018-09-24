/*
    Kotlin solutions to the project Euler Problems
*/
import java.util.Random
import kotlin.math.pow


fun main(args: Array<String>) {
    // Run the nth euler solution
    val euler = Euler()
    euler.prob62()
    println("\n7919 is prime: ${euler.probablyPrime(7919)}")
}


class Euler() {
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

    /** 
    The cube, 41063625 (345^3), can be permuted to produce two other cubes:
    56623104 (384^3) and 66430125 (405^3).In fact, 41063625 is the smallest
    cube which has exactly three permutations of its digits which are also
    cube.
    Find the smallest cube for which exactly five permutations of its digits
    are cube.
    **/
    fun prob62(target: Int = 5) {
        var perms = HashMap<List<Char>, MutableList<Long>>()
        var maxPerms = 1
        var requiredDigits: Int? = null

        var n: Long = 1
        var c: Long

        while (true) {
            c = n * n * n
            n += 1

            var digits = c.toString().toCharArray().sorted()

            if (requiredDigits != null && digits.size > requiredDigits) {
                // We have the minimum solution by now
                break
            }

            // Update the map
            val cubes = perms.getOrDefault(digits, mutableListOf<Long>())
            cubes.add(c)
            perms.put(digits, cubes)

            if (cubes.size > maxPerms) {
                maxPerms = cubes.size
                println("New longest: $maxPerms, $cubes")

                if (maxPerms == target) {
                    requiredDigits = digits.size
                }
            }
        }
        
        // Get the minimal case
        var minCase = c  // Start with the last cube checked as an upper bound

        for ((_, v) in perms.asSequence()) {
            if (v.size == target) {
                val min = v.min()
                if (min!! < minCase) {
                    minCase = min
                }
            }
        }
        println(minCase)
    }
}
