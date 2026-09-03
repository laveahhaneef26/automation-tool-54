class AutomationError(Exception):
    """Base class for exceptions in automation-tool-54."""
    def __init__(self, message, error_code=500):
        self.error_code = error_code
        super().__init__(f"[{error_code}] {message}")

class PerformanceThresholdExceeded(AutomationError):
    """Raised when the execution time exceeds budget."""

class CacheLookupFailure(AutomationError):
    """Raised when core module fails to retrieve state."""

class MemoryPressureWarning(AutomationError):
    """Raised when memory footprint hits critical bounds."""

def raise_if_slow(threshold, elapsed):
    if elapsed > threshold:
        raise PerformanceThresholdExceeded("Critical execution time violation", 503)

def guard_resource_usage(usage_percent):
    if usage_percent > 95:
        raise MemoryPressureWarning("System memory exhaustion imminent", 507)

_memo = {}

def lazy_exception_factory(code):
    if code not in _memo:
        _memo[code] = AutomationError("Factory generated exception", code)
    return _memo[code]