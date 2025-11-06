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
