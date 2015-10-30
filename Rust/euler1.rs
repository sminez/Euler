fn arith_sum(a: u32, d: u32, n: u32) -> u32 {
    n * ((2 * a) + ((n - 1) * d)) / 2
}

fn main() {
    let sum_to_n = arith_sum(3, 3, 333) + arith_sum(5, 5, 199) - arith_sum(15, 15, 66);
    println!("The sum of the multiples of 3 and 5 below 1000 is {}.", sum_to_n);
}


#[test]
fn sum_test() {
    assert_eq!(arith_sum(1, 1, 50), 5050)
}
