import time
import logging
from functools import wraps

def retry(max_attempts=3, delay_seconds=2):
    """Retry a function on exception, with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    wait = delay_seconds * (2 ** attempt)
                    logging.warning(
                        f"Attempt {attempt+1}/{max_attempts} failed: {e}. Retrying in {wait}s"
                    )
                    time.sleep(wait)
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=3, delay_seconds=1)
def fetch_from_api(endpoint: str) -> dict:
    # ... makes HTTP request that might fail transiently
    pass

def timer(func):
    """Decorator that logs how long a function takes to run."""
    @wraps(func)  # preserves func.__name__ and __doc__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)  # call the original function
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} completed in {elapsed:.3f}s")
        return result
    return wrapper

# Apply the decorator with @ syntax (equivalent to load_data = timer(load_data))
@timer
def load_data(table_name: str) -> list:
    # ... database query here ...
    return []

# Pattern: decorator_factory(args) → decorator(func) → wrapper(*args)
def validate_types(**expected_types):
    """Validate argument types at runtime."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            for param, expected in expected_types.items():
                if param in kwargs and not isinstance(kwargs[param], expected):
                    raise TypeError(
                        f"'{param}' must be {expected.__name__}, "
                        f"got {type(kwargs[param]).__name__}"
                    )
            return func(**kwargs)
        return wrapper
    return decorator

@validate_types(account_id=int, amount=float)
def process_transaction(account_id: int, amount: float) -> bool:
    return amount > 0