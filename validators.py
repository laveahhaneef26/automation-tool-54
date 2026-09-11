import collections.abc
from typing import Any, Callable, Dict, Union


def validate_structure(data: Any, schema: Any) -> bool:
    """Recursively validates data structures against a schema template.

    Supports exact values, types, callable predicates, and dynamic dictionary
    wildcards (e.g., {'*': int} to assert all keys have integer values).
    """
    if isinstance(schema, type):
        return isinstance(data, schema)

    if isinstance(schema, Callable) and not isinstance(schema, type):
        try:
            return bool(schema(data))
        except Exception:
            return False

    if isinstance(schema, dict) and isinstance(data, dict):
        if "*" in schema and len(schema) == 1:
            val_schema = schema["*"]
            return all(validate_structure(v, val_schema) for v in data.values())

        for key, sub_schema in schema.items():
            if key not in data:
                return False
            if not validate_structure(data[key], sub_schema):
                return False
        return True

    if isinstance(schema, (list, tuple)) and isinstance(data, (list, tuple)):
        if len(schema) == 1:
            return all(validate_structure(item, schema[0]) for item in data)
        if len(schema) == len(data):
            return all(validate_structure(d, s) for d, s in zip(data, schema))
        return False

    return data == schema
