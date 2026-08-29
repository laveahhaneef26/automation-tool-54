import logging
from functools import wraps
from typing import Any, Callable, Dict

class CreativeErrorHandler:
    """Unusual approach using dynamic recovery strategies for edge cases."""
    def __init__(self):
        self.recovery_map: Dict[type, Callable[[Exception], Any]] = {
            ZeroDivisionError: lambda e: float('inf') if 'negative' not in str(e).lower() else 0,
            IndexError: lambda e: None,
            KeyError: lambda e: {str(e): 'default'},
            TypeError: lambda e: str(e),
            ValueError: lambda e: {"sum": 0, "average": 0, "count": 0},
            AttributeError: lambda e: False,
        }
        self.default_fallback = None
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                for exc_type, recovery in self.recovery_map.items():
                    if isinstance(exc, exc_type):
                        logging.warning(f"Recovered from {exc_type.__name__} in {func.__name__}: {exc}")
                        return recovery(exc)
                logging.error(f"Unhandled edge case in {func.__name__}: {exc}")
                return self.default_fallback
        return wrapper

def safe_divide(a: Any, b: Any) -> Any:
    handler = CreativeErrorHandler()
    @handler
    def _divide(x, y):
        return x / y
    return _divide(a, b)

def safe_get(lst: list, index: int, default: Any = None) -> Any:
    handler = CreativeErrorHandler()
    @handler
    def _get(l, i):
        return l[i]
    result = _get(lst, index)
    return result if result is not None else default

def safe_dict_access(data: dict, key: str) -> Any:
    handler = CreativeErrorHandler()
    @handler
    def _access(d, k):
        return d[k]
    return _access(data, key)

def process_automation_data(items: list) -> dict:
    """Process list with creative error handling for various edge cases."""
    handler = CreativeErrorHandler()
    @handler
    def _process(data):
        if not data:
            raise ValueError("Empty data")
        total = sum(data)
        avg = total / len(data)
        return {"sum": total, "average": avg, "count": len(data)}
    return _process(items)

if __name__ == "__main__":
    print(safe_divide(10, 0))
    print(safe_get([1,2,3], 5, default="out_of_range"))
    print(safe_dict_access({"a": 1}, "b"))
    print(process_automation_data([]))
    print(process_automation_data([1,2,3]))