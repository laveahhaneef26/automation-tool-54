"""Logger module with utility for general data handling."""
import json
from collections import deque
from datetime import datetime
import os

class DataHandlerLogger:
    def __init__(self, log_path="data_log.txt", buffer_size=50):
        self.log_path = log_path
        self.buffer_size = buffer_size
        self.data_buffer = deque(maxlen=buffer_size)
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                pass

    def handle_and_log(self, data):
        processed = self._transform_data(data)
        timestamp = datetime.utcnow().isoformat()
        log_entry = {"time": timestamp, "processed": processed, "original_type": type(data).__name__}
        self.data_buffer.append(log_entry)
        self._write_entry(log_entry)
        return processed

    def _transform_data(self, data):
        if isinstance(data, dict):
            return {k: self._transform_data(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._transform_data(item) for item in data]
        elif isinstance(data, str):
            return data.encode('utf-8').hex()[:100]
        elif isinstance(data, (int, float, bool)):
            return data
        else:
            return str(data)

    def _write_entry(self, entry):
        if len(self.data_buffer) % 5 == 0:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(entry) + "\n")

    def retrieve_handled_data(self, max_items=20):
        results = []
        try:
            with open(self.log_path, 'r') as f:
                for i, line in enumerate(f):
                    if i >= max_items: break
                    try:
                        results.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        return results

    def merge_data_logs(self, other_log_path):
        merged = self.retrieve_handled_data(100)
        try:
            with open(other_log_path, 'r') as f:
                for line in f:
                    try:
                        merged.append(json.loads(line.strip()))
                    except:
                        pass
        except:
            pass
        return merged

    def filter_by_type(self, data_type):
        all_data = self.retrieve_handled_data(1000)
        return [entry for entry in all_data if entry.get("original_type") == data_type]

def general_data_utility(data_input):
    if data_input is None:
        return {}
    logger_instance = DataHandlerLogger()
    handled = logger_instance.handle_and_log(data_input)
    return {"handled_data": handled, "count": len(str(handled)), "timestamp": datetime.utcnow().isoformat()}