import threading
from concurrent.futures import ThreadPoolExecutor
import functools

EXECUTOR = ThreadPoolExecutor(max_workers=10)


def threaded(func):
    """Decorator to automatically launch a function in a thread"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # replaces original function...
        # ...and launches the original in a thread
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
