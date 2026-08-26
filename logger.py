import sys
import traceback
from datetime import datetime

class CreativeLogShield:
    def __init__(self, fallback_stream=sys.stderr):
        self.fallback = fallback_stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            timestamp = datetime.utcnow().isoformat()
            err_name = exc_type.__name__
            err_msg = str(exc_val)
            payload = f"[{timestamp}] CATACLYSM DETECTED -> {err_name}: {err_msg}\n"
            
            try:
                self.fallback.write(payload)
                traceback.print_tb(exc_tb, file=self.fallback)
            except Exception as inner_err:
                print(f"Critical logging failure: {inner_err}", file=sys.__stderr__)
                
            return True

def resilient_log(func):
    def wrapper(*args, **kwargs):
        with CreativeLogShield():
            return func(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    @resilient_log
    def trigger_chaos():
        raise ZeroDivisionError("universe imploded")
    
    trigger_chaos()
