import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()
        self._load_env()

    def _load_env(self) -> None:
        for key in self._data:
            env_val = os.getenv(key.upper())
            if env_val is not None:
                self._data[key] = type(self._data[key])(env_val)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config key {name} not found')

    def merge(self, overrides: Dict[str, Any]) -> None:
        self._data.update(overrides)

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)

if __name__ == '__main__':
    # Example usage for automation-tool-54
    cfg = get_config({'threads': 4, 'mode': 'fast'})
    print(f'Active mode: {cfg.mode}, threads: {cfg.threads}')