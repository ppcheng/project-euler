import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start

        args_repr = ", ".join(repr(arg) for arg in args)
        kwargs_repr = ", ".join(f"{key}={value!r}" for key, value in kwargs.items())
        signature = ", ".join(part for part in (args_repr, kwargs_repr) if part)

        print(f"Function {func.__name__}({signature}) executed in {execution_time:.9f} seconds.")
        return result

    return wrapper


# Helper function to find the set of primes less than an integer n
# Sieve of Eratosthenes Algorithm
def find_all_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [idx for idx, res in enumerate(is_prime) if res]


def find_all_factors(n):
    factors = []
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.append(i)
            factors.append(n // i)
    factors.sort()
    return factors


def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def is_palindrome_number(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x > 0):
        return False
    reverted = 0
    while x > reverted:
        reverted = reverted * 10 + (x % 10)
        x = x // 10
    return (x == reverted) or (x == reverted // 10)
