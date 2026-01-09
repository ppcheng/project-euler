from collections import deque

from utils import find_all_primes, timer


@timer
def sol(n):
    primes = deque(find_all_primes(n))

    # division method
    start = [x for x in range(2, n + 1)]
    ans = 1
    while sum(start) != n - 1:
        divisor = primes[0]
        cur = start.copy()
        for i in range(len(start)):
            if cur[i] != 1 and cur[i] % divisor == 0:
                cur[i] = cur[i] // divisor

        if start == cur:
            primes.popleft()
        else:
            ans *= divisor
        start = cur
    return ans


if __name__ == "__main__":
    print(f"{sol(10)}")
    print(f"{sol(20)}")
