"""Solution for Problem 6."""

from utils import sum_of_natural_number, sum_of_squares, timer


@timer
def sol(n):
    return sum_of_natural_number(n) ** 2 - sum_of_squares(n)


if __name__ == "__main__":
    print(sol(10))
    print(sol(100))
