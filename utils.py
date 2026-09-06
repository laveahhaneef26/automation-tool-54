import functools
import time
import random
from typing import Callable, Any

def retry_with_jitter(retries: int = 3, delay: float = 0.5) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i) + random.uniform(0, 0.1))
            raise last_ex
        return wrapper
    return decorator

def batch_process(iterable: list, size: int) -> list:
    return [iterable[i:i + size] for i in range(0, len(iterable), size)]

def deep_freeze(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(deep_freeze(i) for i in obj)
    if isinstance(obj, dict):
        return {k: deep_freeze(v) for k, v in obj.items()}
    return obj

class SilentDict(dict):
    def __missing__(self, key: Any) -> None:
        return None

def curry(func: Callable) -> Callable:
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *a, **kw: curried(*(args + a), **{**kwargs, **kw})
    return curried