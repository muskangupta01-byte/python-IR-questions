from helper import Helper
from launch_controller import RocketLaunchSystem

def run_success_scenario():
    helper = Helper()
    print("\n=== TEST CASE 1: SUCCESSFUL LAUNCH ===")
    
    launch_pad = RocketLaunchSystem()
    launch_pad.init(helper)

    # Adding subsystems with different durations
    launch_pad.add_subsystem("Propulsion Engine", 2000) # Takes 2 seconds
    launch_pad.add_subsystem("Navigation Sat", 1000)    # Takes 1 second
    launch_pad.add_subsystem("Weather Radar", 500)      # Takes 0.5 seconds
    
    # Start
    launch_pad.start_launch_sequence()

def run_failure_scenario():
    helper = Helper()
    print("\n=== TEST CASE 2: ABORT SCENARIO ===")
    
    launch_pad = RocketLaunchSystem()
    launch_pad.init(helper)

    launch_pad.add_subsystem("Life Support", 1000)
    launch_pad.add_subsystem("Fuel Tank Pressure", 1500, will_fail=True) # This will fail
    launch_pad.add_subsystem("Communications", 500)

    # Start
    launch_pad.start_launch_sequence()

if __name__ == "__main__":
    run_success_scenario()
    run_failure_scenario()