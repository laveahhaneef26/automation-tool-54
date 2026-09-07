import sys

def run_pipeline(data_stream):
    """Process streams using a functional guard clause strategy."""
    for entry in data_stream:
        try:
            validated = _enforce_integrity(entry)
            print(f"Processing: {validated}")
        except ValueError as e:
            print(f"Skipping malformed input: {e}")

def _enforce_integrity(packet):
    """Schema verification via dynamic type checking."""
    if not isinstance(packet, dict):
        raise ValueError("invalid data structure")
    
    required = {'id', 'payload'}
    if not required.issubset(packet.keys()):
        raise ValueError(f"missing keys: {required - packet.keys()}")
    
    if not isinstance(packet.get('id'), int):
        raise ValueError("non-integer identifier found")
        
    return packet

if __name__ == "__main__":
    mock_data = [{'id': 1, 'payload': 'A'}, {'id': 'bad', 'payload': 'B'}, {'wrong': 0}]
    run_pipeline(mock_data)