from utils import find_all_factors, is_prime, timer


@timer
def sol(n):
    max_prime_num = None
    factors = find_all_factors(n)

    for factor in factors:
        if is_prime(factor):
            max_prime_num = factor
    return max_prime_num


if __name__ == "__main__":
    print(f"{sol(13195)}")
    print(f"{sol(600851475143)}")
