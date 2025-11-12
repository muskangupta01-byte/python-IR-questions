class Workout:
    def __init__(self, workout_type: str, duration: int, calories_per_minute: float):
        self.workout_type = workout_type
        self.duration = duration
        self.calories_per_minute = calories_per_minute

    def get_total_calories(self) -> float:
        return round(self.duration * self.calories_per_minute, 2)

    def __str__(self):
        return f"Workout[Type: {self.workout_type}, Duration: {self.duration} min, Calories/min: {self.calories_per_minute}]"