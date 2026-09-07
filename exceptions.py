class AutomationError(Exception):
    """Base exception for automation-tool-54"""

class ConfigMissingError(AutomationError):
    """Raised when core configuration is absent"""

class ExecutionTimeout(AutomationError):
    """Raised when operation exceeds TTL"""

def ensure_safe_execution(func):
    """Decorator for wrapping risky automation blocks"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise AutomationError(f"Failure in {func.__name__}: {str(e)}") from e
    return wrapper

def raise_if_none(value, message="Value cannot be null"):
    """Check for presence before proceeding"""
    if value is None:
        raise AutomationError(message)
    return value

def validate_environment(keys):
    """Check presence of expected environment keys"""
    import os
    missing = [k for k in keys if k not in os.environ]
    if missing:
        raise ConfigMissingError(f"Missing env variables: {', '.join(missing)}")
    return True