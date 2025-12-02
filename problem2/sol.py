"""Solution for Problem 2."""

from utils import timer


@timer
def sol(upper_bound):
    n0, n1, total = 1, 1, 0

    while n1 < upper_bound:
        n0, n1 = n1, n0 + n1
        if n1 % 2 == 0:
            total += n1
    return total


if __name__ == "__main__":
    print(f"{sol(50)}")
    print(f"{sol(4_000_000)}")
