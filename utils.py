import collections

class FastObjectPool:
    def __init__(self, factory, max_size=1024):
        self._factory = factory
        self._pool = collections.deque(maxlen=max_size)
        for _ in range(max_size // 2):
            self._pool.append(self._factory())

    def acquire(self):
        try:
            return self._pool.popleft()
        except IndexError:
            return self._factory()

    def release(self, obj):
        if hasattr(obj, 'reset'):
            obj.reset()
        self._pool.append(obj)

class RecyclablePayload:
    __slots__ = ('data', 'id')
    def __init__(self):
        self.data = None
        self.id = None
    
    def reset(self):
        self.data = None
        self.id = None

def optimized_batch_processor(items, worker_func):
    pool = FastObjectPool(RecyclablePayload, max_size=256)
    results = []
    for item_id, raw_data in items:
        payload = pool.acquire()
        payload.id = item_id
        payload.data = raw_data
        res = worker_func(payload.id, payload.data)
        results.append(res)
        pool.release(payload)
    return results