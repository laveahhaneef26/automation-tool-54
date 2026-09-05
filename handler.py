import functools
import time

class ExecutionCache:
    def __init__(self, ttl=60):
        self._data = {}
        self._ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self._data:
                ts, val = self._data[key]
                if now - ts < self._ttl:
                    return val
            result = func(*args, **kwargs)
            self._data[key] = (now, result)
            return result
        return wrapper

memoize_with_expiry = ExecutionCache

@memoize_with_expiry(ttl=30)
def heavy_computation(data_node: dict) -> int:
    # Simulate high latency logic
    accumulator = 0
    for i in range(10000):
        accumulator += hash(str(data_node) + str(i))
    return accumulator % 1024

def process_request(payload: dict):
    try:
        return heavy_computation(payload)
    except Exception as e:
        return f"error: {str(e)}"

if __name__ == '__main__':
    data = {'id': 54, 'status': 'active'}
    print(process_request(data))