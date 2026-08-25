import time
from collections import deque
class CoreProcessor:
    def __init__(self, max_cache_size=100):
        self.cache = {}
        self.cache_order = deque(maxlen=max_cache_size)
    def _add_to_cache(self, key, value):
        if key in self.cache:
            self.cache_order.remove(key)
        elif len(self.cache_order) == self.cache_order.maxlen:
            oldest = self.cache_order.popleft()
            del self.cache[oldest]
        self.cache[key] = value
        self.cache_order.append(key)
    def optimized_compute(self, key, data):
        if key in self.cache:
            return self.cache[key]
        result = 0
        for i in range(1000):
            temp = sum(data)
            result += (temp * i) % 100
        self._add_to_cache(key, result)
        return result
    def batch_process(self, tasks):
        results = []
        for task in tasks:
            if not isinstance(task, dict):
                continue
            key = task.get('id')
            data = task.get('data', [])
            if key is None:
                continue
            result = self.optimized_compute(key, data)
            results.append(result)
        return results
    def clear_cache(self):
        self.cache.clear()
        self.cache_order.clear()

if __name__ == "__main__":
    processor = CoreProcessor()
    tasks = [{'id': i, 'data': list(range(50))} for i in range(20)]
    start = time.time()
    results = processor.batch_process(tasks)
    first_run = time.time() - start
    print(f"First run time: {first_run:.4f} seconds")
    start = time.time()
    results = processor.batch_process(tasks)
    second_run = time.time() - start
    print(f"Second run time: {second_run:.4f} seconds")
    if second_run > 0:
        print(f"Speedup: {first_run / second_run:.1f}x")