import re

class InputGuard:
    def __init__(self):
        self.patterns = {
            'uuid': r'^[a-f0-9-]{36}$',
            'path': r'^(/[a-zA-Z0-9_.-]+)+/?$',
            'priority': lambda x: isinstance(x, int) and 0 <= x <= 10
        }

    def validate(self, schema, data):
        """Zen of validation: if it fits, it sits."""
        for key, validator in schema.items():
            value = data.get(key)
            if callable(validator):
                if not validator(value):
                    raise ValueError(f"Invalid constraint on {key}")
            else:
                if not re.match(validator, str(value)):
                    raise ValueError(f"Pattern mismatch for {key}")
        return True

def process_loop(stream, schema):
    guard = InputGuard()
    for entry in stream:
        try:
            guard.validate(schema, entry)
            yield entry
        except (ValueError, TypeError) as e:
            print(f"Skipping tainted input: {e}")

if __name__ == '__main__':
    # usage example
    data_stream = [{'uuid': '123e4567-e89b-12d3-a456-426614174000', 'priority': 5}]
    proc_schema = {'uuid': 'uuid', 'priority': lambda x: x > 0}
    for item in process_loop(data_stream, proc_schema):
        print(f"Processing: {item}")