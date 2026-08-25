from collections import deque
from typing import Any, Callable, Deque, List, Optional

def general_data_handler(data: Any, processors: Optional[List[Callable[[Any], Any]]] = None) -> Any:
    if processors is None:
        processors = []
    queue: Deque[Any] = deque([data])
    for processor in processors:
        new_queue: Deque[Any] = deque()
        while queue:
            item = queue.popleft()
            processed = processor(item)
            if isinstance(processed, (list, tuple)):
                new_queue.extend(processed)
            else:
                new_queue.append(processed)
        queue = new_queue
    if len(queue) == 1:
        return queue[0]
    return list(queue)

def _flatten_processor(item: Any) -> Any:
    if isinstance(item, dict):
        flat = {}
        for k, v in item.items():
            if isinstance(v, dict):
                for subk, subv in v.items():
                    flat[f"{k}_{subk}"] = subv
            else:
                flat[k] = v
        return flat
    return item

def _stringify_processor(item: Any) -> Any:
    if isinstance(item, (int, float, bool)):
        return str(item)
    if isinstance(item, dict):
        return {k: _stringify_processor(v) for k, v in item.items()}
    if isinstance(item, list):
        return [_stringify_processor(x) for x in item]
    return item

def _dedup_processor(item: Any) -> Any:
    if isinstance(item, list):
        seen = set()
        result = []
        for x in item:
            sx = str(x)
            if sx not in seen:
                seen.add(sx)
                result.append(x)
        return result
    return item

def handle_general_data(data: Any) -> Any:
    processors = [_flatten_processor, _stringify_processor, _dedup_processor]
    return general_data_handler(data, processors)