"""Solution for Problem 7."""

from utils import is_prime, timer


@timer
def sol(n):
    if n == 1:
        return 2
    count = 1
    num = 3
    while count < n:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 2


if __name__ == "__main__":
    print(sol(6))
    print(sol(10001))
