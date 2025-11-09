from queue import Queue

from utils import is_palindrome_number, timer


@timer
def sol(n):
    i, j = pow(10, n) - 1, pow(10, n) - 1

    queue = Queue()
    queue.put((i, j))
    seen = set()
    while queue.qsize() > 0:
        i, j = queue.get()
        if (i, j) in seen:
            continue
        if is_palindrome_number(i * j):
            return (i, j)
        seen.add((i, j))
        queue.put((min(i, j - 1), max(i, j - 1)))
        queue.put((min(i - 1, j), max(i - 1, j)))
    return None


if __name__ == "__main__":
    print(f"{sol(2)}")
    print(f"{sol(3)}")
