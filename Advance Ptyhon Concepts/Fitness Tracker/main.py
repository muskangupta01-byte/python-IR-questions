from workout import Workout
from user import User

if __name__ == "__main__":
    # Create users
    user1 = User("U101", "Aditi")
    user2 = User("U102", "Rohan")

    # Create workouts
    run = Workout("Running", 30, 10)
    cycle = Workout("Cycling", 45, 8)
    yoga = Workout("Yoga", 60, 5)

    # Add workouts
    user1.add_workout(run)
    user1.add_workout(yoga)
    user2.add_workout(cycle)

    # Display summaries
    user1.display_workouts()
    user2.display_workouts()


#sample output
"""
Workouts for Aditi:
  Workout[Type: Running, Duration: 30 min, Calories/min: 10]
  Workout[Type: Yoga, Duration: 60 min, Calories/min: 5]
Total Calories Burned: 600.0

Workouts for Rohan:
  Workout[Type: Cycling, Duration: 45 min, Calories/min: 8]
Total Calories Burned: 360.0
"""