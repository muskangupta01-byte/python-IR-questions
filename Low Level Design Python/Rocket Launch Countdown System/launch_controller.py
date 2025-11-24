import threading
from typing import List
from helper import Helper
from models import Subsystem

class RocketLaunchSystem:
    def __init__(self):
        self.helper = None
        self.subsystems: List[Subsystem] = []

    def init(self, helper: Helper):
        self.helper = helper
        self.subsystems = []
        self.helper.log("Rocket Launch System Initialized.")

    def add_subsystem(self, name: str, duration_ms: int, will_fail: bool = False):
        system = Subsystem(name, duration_ms, will_fail, self.helper)
        self.subsystems.append(system)

    def start_launch_sequence(self):
        self.helper.log("--- Initiating Pre-Launch Checks ---")
        
        active_threads = []

        # 1. Create and Start Threads
        for system in self.subsystems:
            t = threading.Thread(target=system.perform_check)
            t.start()
            active_threads.append(t)

        # 2. Wait for Completion (The Join Approach)
        # The main thread stops here and waits for thread 1, then thread 2, etc.
        for t in active_threads:
            t.join()

        self.helper.log("--- All Checks Complete. Evaluating Status ---")
        
        # 3. Aggregate Results
        # Because we joined, we know all systems have finished updating their status.
        all_systems_go = True
        failed_systems = []

        for system in self.subsystems:
            if system.status != "GO":
                all_systems_go = False
                failed_systems.append(system.name)

        # 4. Final Decision
        if all_systems_go:
            self.helper.log("STATUS: ALL SYSTEMS GO. LAUNCHING!")
        else:
            self.helper.log(f"STATUS: ABORT MISSION. Failures detected in: {failed_systems}")