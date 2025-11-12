from workout import Workout

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.workouts = []

    def add_workout(self, workout: Workout):
        self.workouts.append(workout)

    def get_total_calories(self) -> float:
        return round(sum(w.get_total_calories() for w in self.workouts), 2)

    def display_workouts(self):
        print(f"\nWorkouts for {self.name}:")
        if not self.workouts:
            print("  No workouts logged yet.")
        else:
            for w in self.workouts:
                print(f"  {w}")
        print(f"Total Calories Burned: {self.get_total_calories()}")