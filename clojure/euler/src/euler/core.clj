(ns euler.core
  (:use [clojure.algo.generic.functor :only [fmap]] :reload)
  (:require [clojure.math.numeric-tower :as math])
  (:gen-class))

(def lazy-fibs
  "A lazy infinite Fibonacci sequence"
  (lazy-seq (map first (iterate (fn [[a b]] [b (+ a b)]) [1 1]))))

(def lazy-primes
    "An infinite generator of primes based on a sieve that stores each prime
     indexed against its current greatest multiple. This improves performance
     in two ways:
        1. Uses a map for the sieve so the actual lookup is faster
        2. The sieve only stores - in effect - the next value that needs to be
           skipped for each prime divisor, so memory usage should be better."
  (letfn [(update-sieve [previous current-sieve prime]
            (update current-sieve (+ prime previous) conj prime))
          (next-prime [sieve k]
            ;; k_factors is a list of prime factors. It is not guaranteed to be
            ;; *all* of the prime factors of k: only those where k is the current
            ;; largest multiple of prime p in the sieve.
            (let [k-factors (get sieve k)]
              (if (nil? k-factors)
                ;; k is a prime so return it and mark its square in the sieve
                ;; for later filtering and cons it to the list of known primes.
                ;; >> This is valid for all primes p as all multiples of p
                ;;    below p^2 will be a composite pq where q is less than p.
                (lazy-seq (cons k (next-prime (assoc sieve (* k k) (list k)) (inc k))))
                ;; k is the current highest multiple of at least one prime
                ;; stored in the sieve.
                ;; >> Remove k from the sieve and move each of its associated
                ;;    prime factors to their next highest multiple.
                (next-prime
                 (reduce (partial update-sieve k) (dissoc sieve k) k-factors)
                 (inc k)))))]
    ;; Kick it off with an empty sieve and 2 as the first value for k
    (next-prime {} 2)))

(defn p-factors
  "Return the prime factors of k in ascending order"
  [k]
  (loop [candidates (take (-> k math/sqrt int inc) lazy-primes)
         dividend k
         k-factors []]
    (if (or (= dividend 1) (empty? candidates))
      (case dividend
        ;; Ensure that primes return themselves
        1 (if (empty? k-factors) [k] k-factors)
        ;; There is (at most) one prime factor that is > sqrt k
        (conj k-factors dividend))
      (let [divisor (first candidates)
            remainder (/ dividend divisor)]
        (if (integer? remainder)
          (recur candidates remainder (conj k-factors divisor))
          (recur (rest candidates) dividend k-factors))))))

(defn pal?
  "Return true if the argument is a palindrome"
  [a]
  (= (apply str (reverse (str a))) (str a)))

(defn n-digit-pals
  "All n-digit palindrome numbers"
  [n]
  (let [digits (map str (range 9 -1 -1))
        to-int (fn [x] (BigInteger. x))
        no-leading-zero (fn [x] (not= \0 (first x)))]
    (case n
      1 (map to-int digits)
      2 (map to-int (for [k digits] (str k k)))
      (map to-int (filter no-leading-zero (for [k digits m (n-digit-pals (- n 2))] (str k m k)))))))

(defn to-digits
  "Return a vector of the digits for a positive int"
  [n]
  (if (pos? n)
    (conj (to-digits (quot n 10)) (mod n 10)) []))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defn euler1
  "Find the sum of the multiples of α and β below γ"
  [α β γ]
  (letfn [(m-sum [mult ubound]
            (let [m mult
                  n (quot (- ubound 1) mult)]
              ;; n/2(2a+(n-1)d) -> nm/2(2+n-1)
              (* (/ (* n m) 2) (- (+ 2 n) 1))))]
    (int (- (+ (m-sum α γ) (m-sum β γ)) (m-sum (* α β) γ)))))

(defn euler2
  "Sum of the even terms of the Fibonacci sequence below an upper bound"
  [upper]
  (reduce + (filter even? (take-while #(< % upper) lazy-fibs))))

(defn euler3
  "Find the largest prime factor of a number"
  [n]
  (apply max (p-factors n)))

(defn euler4-slow
  "Find the largest palendromic product of two n-digit numbers"
  [n]
  (let [upper (math/expt 10 n)
        step-size (min 1000 (int (* upper 0.1)))]
    (loop [x-upper upper
           x-lower (- upper step-size)
           y-upper x-upper
           y-lower x-lower
           stepped false]
      (let [solutions
            (filter pal?
                    (for [x (range x-lower x-upper)
                          y (range y-lower y-upper)]
                      (* x y)))]
        (if-not (empty? solutions)
          (apply max solutions)
          (if-not stepped
            (recur x-upper x-lower x-lower (- x-lower step-size) true)
            (recur x-upper y-lower y-upper y-lower false)))))))

(defn euler4
  "Find the largest palendromic product of two n-digit numbers"
  [n]
  ;; Multiplying two n-digit numbers gives a range of 10^2n-1 -> 10^2n
  (let [cands (n-digit-pals (* 2 n))
        cands2 (n-digit-pals (- (* 2 n) 1))
        has-valid-factors (fn [x] (every? #(< % (math/expt 10 n)) (p-factors x)))]
    (first (filter has-valid-factors cands))))

(defn euler5
  "Find the smallest integer than can be evenly divided by 1..n"
  [n]
  (let [keep-max (fn [current-map [k v]]
                   (let [current-v (get current-map k)]
                     (if (or (nil? current-v) (> v current-v))
                       (assoc current-map k v)
                       current-map)))
        freqs (map frequencies (map p-factors (range 1 (+ n 1))))
        factors (seq (reduce keep-max {} (apply concat (map seq freqs))))]
    (reduce (fn [total [prime count]] (* total (math/expt prime count))) 1 factors)))

(defn euler9
  "Find the product abc where (a b c) is a Pythagorean Triple
   and the sum a+b+c == target.
   Returns a tuple of ((a b c) product)"
  [target]
  (letfn [(candidate [c]
            (let [c2 (* c c)]
              (first (for [a (range 1 c) :let [b (Math/sqrt (- c2 (* a a)))]
                           :when (== (int b) b)]
                       [a (int b) c]))))
          (check-solution [target candidate]
            (if-not (nil? candidate)
              (let [quotient (/ target (reduce + candidate))]
                (if (integer? quotient)
                  (map #(* quotient %) candidate)))))]
    (let [solution (first (filter (complement nil?)
                                  (map
                                   (comp (partial check-solution target) candidate)
                                   (range 5 (- target 2)))))]
      (if-not (nil? solution)
        (list solution (reduce * solution))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defn -main
  [& args]
  (println "1:: Sum of multiples of 3 and 5 below 1000")
  (println (euler1 3 5 1000))
  (println "\n2:: Sum of even fibonacci numbers below 4 million")
  (println (euler2 4000000))
  (println "\n3:: Largest prime factor of 600851475143")
  (println (euler3 600851475143))
  (println "\n9:: Product abc for Pythogarean triple (a b c) where a+b+c=10000")
  (println (euler9 10000)))
  
