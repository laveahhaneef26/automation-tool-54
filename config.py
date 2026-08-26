import os
from typing import Any, Dict

class MagicConfig(dict):
    def __getattr__(self, key: str) -> Any:
        try:
            val = self[key]
            return MagicConfig(val) if isinstance(val, dict) else val
        except KeyError as err:
            raise AttributeError(f"Missing config key: {err}")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]) -> None:
        self._defaults = defaults

    def load(self, override_env_prefix: str = "APP_") -> MagicConfig:
        merged = self._deep_copy(self._defaults)
        for key, val in os.environ.items():
            if key.startswith(override_env_prefix):
                config_key = key[len(override_env_prefix):].lower()
                merged[config_key] = self._parse_val(val)
        return MagicConfig(merged)

    def _deep_copy(self, d: Dict[str, Any]) -> Dict[str, Any]:
        return {k: (self._deep_copy(v) if isinstance(v, dict) else v) for k, v in d.items()}

    def _parse_val(self, val: str) -> Any:
        if val.lower() in ("true", "yes", "1"): return True
        if val.lower() in ("false", "no", "0"): return False
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val

def load_config(defaults: Dict[str, Any]) -> MagicConfig:
    return ConfigLoader(defaults).load()