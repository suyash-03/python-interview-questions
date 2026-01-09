def decorator(func):
    def wrapper(*args, **kwargs):   # handles any # of args
        print("Calling:", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@decorator
def add(a, b):
    return a+b

print(add(5, 3))



import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Time:", time.time() - start)
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()