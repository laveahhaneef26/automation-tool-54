import time
import functools
from pathlib import Path
import json

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def atomic_write(filepath, data):
    """Writes data to a temp file then renames to avoid corruption."""
    p = Path(filepath)
    tmp = p.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(data, f)
    tmp.rename(p)

def memoize_to_disk(cache_file):
    def decorator(func):
        cache = {}
        if Path(cache_file).exists():
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        @functools.wraps(func)
        def wrapper(*args):
            key = str(args)
            if key not in cache:
                cache[key] = func(*args)
                atomic_write(cache_file, cache)
            return cache[key]
        return wrapper
    return decorator

def pipeline(*funcs):
    def execute(x):
        return functools.reduce(lambda v, f: f(v), funcs, x)
    return execute