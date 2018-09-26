/*
    Kotlin solutions to the project Euler Problems
*/
import euler.*

fun main(args: Array<String>) {
    // Run the nth euler solution
    val euler = Euler()
    euler.prob62()

    println(primes().take(100).toList())
    println(primesToN(100))
    println(pFactors(987654321))
}


class Euler() {
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
