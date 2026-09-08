import functools
import logging
import time
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logging.info(f"{func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper

def flatten_nested_data(data: list[Any]) -> list[Any]:
    accumulator = []
    for item in data:
        if isinstance(item, list):
            accumulator.extend(flatten_nested_data(item))
        else:
            accumulator.append(item)
    return accumulator

class DataSanitizer:
    def __init__(self, key_map: dict[str, str]):
        self.key_map = key_map

    def clean(self, dirty_dict: dict[str, Any]) -> dict[str, Any]:
        return {self.key_map.get(k, k): v for k, v in dirty_dict.items() if v is not None}

def retry_operation(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator