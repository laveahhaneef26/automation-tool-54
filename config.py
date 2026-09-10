import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, default_path: str = "defaults.json"):
        self.defaults = self._load_json(default_path)
        self.config = self.defaults.copy()

    def _load_json(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def merge_env(self, prefix: str = "APP_") -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self.config[clean_key] = self._try_cast(value)

    def _try_cast(self, val: str) -> Any:
        try:
            return json.loads(val.lower())
        except (json.JSONDecodeError, TypeError):
            return val

    def __getitem__(self, key: str) -> Any:
        return self.config.get(key)

    def __repr__(self) -> str:
        return f"ConfigStore({list(self.config.keys())})"

# usage for automation-tool-54
def get_app_config():
    loader = ConfigLoader()
    loader.merge_env()
    return loader