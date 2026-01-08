"""Solution for Problem 10."""

from utils import find_all_primes, timer


@timer
def sol(n: int):
    return sum(find_all_primes(n))


if __name__ == "__main__":
    print(sol(10))
    print(sol(2_000_000))
