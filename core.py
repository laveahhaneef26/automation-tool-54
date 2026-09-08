import functools
import time
from typing import Callable, Any, List, Dict

class FastExecutionPipeline:
    __slots__ = ('_transforms', '_compiled_chain')

    def __init__(self):
        self._transforms: List[Callable[[Any], Any]] = []
        self._compiled_chain: Callable[[Any], Any] = lambda x: x

    def register(self, fn: Callable[[Any], Any]) -> 'FastExecutionPipeline':
        self._transforms.append(fn)
        self._recompile()
        return self

    def _recompile(self) -> None:
        chain = lambda x: x
        for fn in reversed(self._transforms):
            chain = (lambda f, g: lambda x: f(g(x)))(fn, chain)
        self._compiled_chain = chain

    def execute_batch(self, items: List[Any]) -> List[Any]:
        runner = self._compiled_chain
        return [runner(item) for item in items]

def benchmark_pipeline(pipeline: FastExecutionPipeline, data: List[int]) -> Dict[str, float]:
    start = time.perf_counter()
    results = pipeline.execute_batch(data)
    elapsed = time.perf_counter() - start
    return {"processed_count": len(results), "execution_time_sec": elapsed}