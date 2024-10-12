from json import dumps
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__!r} took: {end_time-start_time:.4f} sec")
        return result
    return wrapper


def pprint(*values):
    for value in values:    
        print(
            dumps(
                value,
                skipkeys=True,
                indent=4
            )
        )
    print()

