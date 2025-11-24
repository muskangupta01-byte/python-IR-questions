import time
from helper import Helper

class Subsystem:
    def __init__(self, name: str, duration_ms: int, will_fail: bool, helper: Helper):
        self.name = name
        self.duration_seconds = duration_ms / 1000.0
        self.will_fail = will_fail
        self.helper = helper
        self.status = "PENDING"  # PENDING, GO, NO_GO

    def perform_check(self):
        """
        This method will be the target for the thread.
        """
        self.helper.log(f"[{self.name}] Check started... (Duration: {self.duration_seconds}s)")
        
        # Simulate processing time
        time.sleep(self.duration_seconds)
        
        if self.will_fail:
            self.status = "NO_GO"
            self.helper.log(f"[{self.name}] Check FAILED!")
        else:
            self.status = "GO"
            self.helper.log(f"[{self.name}] Check PASSED.")