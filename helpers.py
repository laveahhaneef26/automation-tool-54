import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('automation-tool-54')

class UnrecoverableError(Exception):
    """Custom sentinel for non-retryable logical failures."""
    pass

def robust_execution(retries: int = 3):
    """Decorator implementing aggressive error containment and strategy."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except UnrecoverableError as e:
                    logger.critical(f"Hard failure: {e}")
                    raise
                except Exception as e:
                    last_ex = e
                    logger.warning(f"Attempt {attempt} failed: {e}")
            logger.error("Exhausted all recovery attempts")
            raise last_ex
        return wrapper
    return decorator

def safe_access(data: dict, key: str, fallback: Any = None) -> Any:
    """Chainable deep dictionary traversal with defensive defaulting."""
    try:
        keys = key.split('.')
        for k in keys:
            data = data[k]
        return data
    except (KeyError, TypeError, AttributeError):
        return fallback

def dynamic_validator(obj: Any, predicate: Callable[[Any], bool]) -> bool:
    """Predicate-based verification for volatile edge case inputs."""
    try:
        return bool(predicate(obj))
    except Exception:
        return False