import threading
from typing import Any, Dict, Optional

class BaseAutomationException(Exception):
    __slots__ = ('message', 'code', 'context')
    _instances: Dict[str, 'BaseAutomationException'] = {}
    _lock = threading.RLock()

    def __new__(cls, message: str, code: int = 0, context: Optional[Dict[str, Any]] = None):
        key = f"{cls.__name__}:{message}:{code}"
        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                object.__setattr__(instance, 'message', message)
                object.__setattr__(instance, 'code', code)
                object.__setattr__(instance, 'context', context or {})
                cls._instances[key] = instance
            return cls._instances[key]

    def __init__(self, message: str, code: int = 0, context: Optional[Dict[str, Any]] = None):
        if getattr(self, 'message', None) != message:
            object.__setattr__(self, 'message', message)
            object.__setattr__(self, 'code', code)
            object.__setattr__(self, 'context', context or {})
        super().__init__(message)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'code': self.code,
            'context': self.context
        }

class ConfigurationException(BaseAutomationException):
    def __init__(self, message: str, code: int = 100, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, context)

class ProcessingException(BaseAutomationException):
    def __init__(self, message: str, code: int = 200, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, context)

class ValidationException(BaseAutomationException):
    def __init__(self, message: str, code: int = 300, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, context)

class NetworkException(BaseAutomationException):
    def __init__(self, message: str, code: int = 400, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, context)

class CoreOptimizationException(BaseAutomationException):
    def __init__(self, message: str, code: int = 500, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, context)

def clear_exception_cache() -> None:
    with BaseAutomationException._lock:
        BaseAutomationException._instances.clear()

def get_exception_stats() -> Dict[str, int]:
    return {
        'cached_exceptions': len(BaseAutomationException._instances)
    }