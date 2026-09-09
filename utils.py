import json
from typing import Any, Dict, Union
from functools import reduce

def traverse_dict(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """navigates deep dict structures using dot notation"""
    try:
        return reduce(lambda d, key: d.get(key, {}), path.split('.'), data)
    except AttributeError:
        return default

def serialize_and_clean(payload: Any) -> str:
    """sanitized json conversion with recursive key flattening"""
    def flattener(obj):
        if isinstance(obj, dict):
            return {str(k): flattener(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [flattener(i) for i in obj]
        return obj
    return json.dumps(flattener(payload))

class DataPipeline:
    def __init__(self, initial_data: Dict[str, Any]):
        self.storage = initial_data

    def __call__(self, key_path: str, value: Any) -> 'DataPipeline':
        keys = key_path.split('.')
        target = self.storage
        for key in keys[:-1]:
            target = target.setdefault(key, {})
        target[keys[-1]] = value
        return self