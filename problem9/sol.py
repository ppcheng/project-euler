"""Solution for Problem 9."""

from utils import timer


@timer
def sol(total):
    # total = 1000
    # b = 1000*(1000 - 2*a) / 2*(1000 - a)
    # c = 1000 - b - a
    # a < b < c and a + b + c = 1000 => a < 1000 / 3
    for a in range(1, total // 3):
        denominator = total * (total - 2 * a)
        numerator = 2 * (total - a)
        if numerator != 0 and denominator % numerator == 0:
            b = denominator // numerator
            c = total - b - a
            if a < b < c:
                return a * b * c
    return None


if __name__ == "__main__":
    print(sol(1000))
