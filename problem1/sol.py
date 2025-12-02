"""Solution for Problem 1."""

from utils import timer


@timer
def sol(n, divisor1, divisor2):
    # n must be a natural number, i.e. it can't be negative
    if n < 0:
        return 0
    if n < min(divisor1, divisor2):
        return 0
    multiples = []
    for i in range(n):
        if i % divisor1 == 0 or i % divisor2 == 0:
            multiples.append(i)
    total = 0
    for num in multiples:
        total += num
    return total


if __name__ == "__main__":
    print(f"{sol(10, 3, 5)}")
    print(f"{sol(1000, 3, 5)}")
