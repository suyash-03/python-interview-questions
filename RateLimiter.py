import time

cache = {}
TTL = 60  # Time-to-live for each user in seconds

def is_request_allowed(user_id: str) -> bool:
    current_time = time.time()
    if user_id in cache:
        # Remove timestamps older than TTL
        cache[user_id] = [t for t in cache[user_id] if current_time - t < TTL]
        if len(cache[user_id]) < 5:
            cache[user_id].append(current_time)
            return True
        else:
            return False
    else:
        cache[user_id] = [current_time]
        return True
    
if __name__ == "__main__":
    user = "user_123"
    for i in range(7):
        if is_request_allowed(user):
            print(f"Request {i+1} for {user} is allowed.")
        else:
            print(f"Request {i+1} for {user} is denied due to rate limiting.")
        time.sleep(1)  # Simulate time between requests