fn fib(upper_bound: u32) -> u32 {
    match upper_bound {
        0 => 0,
        1 => 1,
        _ => fib(upper_bound - 1) + fib(upper_bound - 2),
    }
}

fn main() {
    let result = fib(10);
    println!("{}", result);
}
