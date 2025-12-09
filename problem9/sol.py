"""Solution for Problem 9."""

from utils import timer


@timer
def sol():
    total = 1000
    for a in range(1, total - 2):
        for b in range(a + 1, total - 1):
            c = total - a - b
            if a**2 + b**2 == c**2:
                return a * b * c


if __name__ == "__main__":
    print(sol())
