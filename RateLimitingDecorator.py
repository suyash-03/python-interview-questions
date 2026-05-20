import time
from functools import wraps

def rate_limiter(seconds):
    # This variable lives in the closure for the decorate function
    last_used = 0
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_used
            now = time.time()
            
            if now - last_used < seconds:
                print(f"API Rate Limited. Please wait {seconds - (now - last_used):.2f}s")
                return None # Stop execution
            
            last_used = now
            return func(*args, **kwargs)
        return wrapper
    return decorator

# The decorator MUST go here
@rate_limiter(5)    
def api():
    print("API Called Successfully")

if __name__ == "__main__":
    api() # First call - Success
    
    time.sleep(2)
    
    api() # Second call (2s later) - Rate Limited