import threading
import time

class Helper:
    def __init__(self):
        self._lock = threading.Lock()

    def log(self, message: str):
        with self._lock:
            # Adding timestamp for clarity
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{timestamp}] {message}")