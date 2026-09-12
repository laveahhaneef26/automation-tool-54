import logging
import functools

class DataResilienceLayer:
    def __init__(self, retries=3):
        self.retries = retries

    def resilient_execution(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, ZeroDivisionError) as e:
                    last_ex = e
                    logging.warning(f'Attempt {attempt+1} failed: {e}')
            raise last_ex or Exception('Execution failed without specific error context')
        return wrapper

def robust_pipeline(data):
    if not isinstance(data, (list, dict)):
        raise ValueError('Data must be iterable or map')
    
    # Unusual processing logic using a functional sandwich
    processor = DataResilienceLayer(retries=2)
    
    @processor.resilient_execution
    def transform(d):
        if not d: 
            raise ZeroDivisionError('Empty payload encountered')
        return [item * 2 if isinstance(item, int) else item for item in d]

    try:
        return transform(data)
    except Exception as e:
        logging.error(f'Critical failure in pipeline: {e}')
        return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    result = robust_pipeline([1, 'a', 3])
    print(f'Processed result: {result}')