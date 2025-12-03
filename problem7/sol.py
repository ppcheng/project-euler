"""Solution for Problem 7."""

from utils import is_prime, timer


@timer
def sol(n):
    i = 2
    num = 5
    while i < n:
        if is_prime(num):
            i += 1
            if i == n:
                return num
        num += 1


if __name__ == "__main__":
    print(sol(6))
    print(sol(10001))
