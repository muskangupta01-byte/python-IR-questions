class WaterTracker:
    def __init__(self, user_name, daily_intake, recommended_intake):
        """
        Initializes a WaterTracker instance.

        Parameters:
            user_name (str): Name of the user
            daily_intake (list of float): List of water intake values (in liters) for each day of a week
            recommended_intake (float): Recommended daily intake in liters
        """
        self.user_name = user_name
        self.daily_intake = daily_intake
        self.recommended_intake = recommended_intake

    def get_total_intake(self):
        """Returns the total water intake for the week."""
        return round(sum(self.daily_intake), 2)

    def get_average_intake(self):
        """Returns the average daily intake (rounded to 2 decimal places)."""
        if not self.daily_intake:
            return 0.0
        return round(sum(self.daily_intake) / len(self.daily_intake), 2)

    def get_days_met_goal(self):
        """Returns the number of days where daily intake meets or exceeds the goal."""
        return sum(1 for day in self.daily_intake if day >= self.recommended_intake)

    def summary(self):
        """Returns a formatted summary of the users hydration report."""
        total = self.get_total_intake()
        average = self.get_average_intake()
        days_met = self.get_days_met_goal()

        # Determine hydration status
        if days_met >= 6:
            status = "Excellent"
        elif days_met >= 4:
            status = "Good"
        else:
            status = "Needs Improvement"

        # Return formatted summary
        return (
            f"User: {self.user_name}\n"
            f"Total Weekly Intake: {total} L\n"
            f"Average Daily Intake: {average} L\n"
            f"Days Goal Met: {days_met}/7\n"
            f"Hydration Status: {status}"
        )

if __name__ == "__main__":
    tracker = WaterTracker("Malti", [2.5, 3.0, 2.0, 2.8, 3.2, 1.9, 2.6], 2.5)
    print(tracker.summary())

#sample output
"""User: Malti
Total Weekly Intake: 18.0 L
Average Daily Intake: 2.57 L
Days Goal Met: 5/7
Hydration Status: Good"""