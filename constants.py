from typing import Any, Tuple


class ImmutableMeta(type):
    """Metaclass enforcing absolute runtime immutability on class attributes."""

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError(
            f"Class '{cls.__name__}' is frozen; constant '{name}' cannot be mutated."
        )

    def __delattr__(cls, name: str) -> None:
        raise TypeError(
            f"Class '{cls.__name__}' is frozen; constant '{name}' cannot be deleted."
        )


class EngineConstants(metaclass=ImmutableMeta):
    """Immutable execution constraints for the automation engine.

    Provides explicit type annotations and strict runtime write-protection.
    """

    TIMEOUT: int = 30
    RETRY_COUNT: int = 5
    AGENT_NAME: str = "automation-tool-54"
    ALLOWED_SCHEMES: Tuple[str, ...] = ("http", "https")
