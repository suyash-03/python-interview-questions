from abc import ABC, abstractmethod
import time
import threading

class RateLimiterStrategy(ABC):
    @abstractmethod
    def allow_request(self, tokens_requested: int = 1) -> bool:
        """
        Evaluates if a request can be processed based on token availability.
        """
        pass

class TokenBucketRateLimiter(RateLimiterStrategy):
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate  # Tokens per second
        self.tokens = float(max_tokens)
        self.last_refill_time = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        """
        Lazily updates the token count based on the elapsed time.
        Must be called within a thread lock to prevent race conditions on self.tokens.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time
        
        if elapsed_time > 0:
            # Calculate tokens earned since last request
            tokens_to_add = elapsed_time * self.refill_rate
            # Caps the bucket at maximum capacity
            self.tokens = min(self.max_tokens, self.tokens + tokens_to_add)
            self.last_refill_time = current_time

    def allow_request(self, tokens_requested: int = 1) -> bool:
        """
        Thread-safe method to check and consume tokens.
        """
        with self.lock:
            self._refill()  # Bring token count up to date
            
            if self.tokens >= tokens_requested:
                self.tokens -= tokens_requested
                return True
            
            return False

class RateLimiterManager:
    """
    Centralized registry to manage rate limits per key (user_id, IP, or endpoint).
    """
    def __init__(self):
        self._limiters = {}
        self._lock = threading.Lock()

    def get_limiter(self, key: str, max_tokens: int, refill_rate: float) -> TokenBucketRateLimiter:
        # Double-checked locking pattern for performance stability
        if key not in self._limiters:
            with self._lock:
                if key not in self._limiters:
                    self._limiters[key] = TokenBucketRateLimiter(max_tokens, refill_rate)
        return self._limiters[key]

# --- Quick Verification Script ---
if __name__ == "__main__":
    # Max 3 tokens, refills at 1 token per second
    limiter = TokenBucketRateLimiter(max_tokens=3, refill_rate=1.0)
    
    # Burst requests
    print(f"Request 1: {limiter.allow_request()}")  # True (3 -> 2 tokens)
    print(f"Request 2: {limiter.allow_request()}")  # True (2 -> 1 tokens)
    print(f"Request 3: {limiter.allow_request()}")  # True (1 -> 0 tokens)
    print(f"Request 4: {limiter.allow_request()}")  # False (0 tokens available)
    
    # Wait 2 seconds to allow a partial refill
    print("\n...Waiting 2 seconds...")
    time.sleep(2)
    
    print(f"Request 5: {limiter.allow_request()}")  # True (Refilled to ~2 tokens, drops to 1)
    print(f"Request 6: {limiter.allow_request()}")  # True (Drops to 0)
    print(f"Request 7: {limiter.allow_request()}")  # False (Exhausted)