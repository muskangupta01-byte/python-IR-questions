class CalorieTracker:
    def __init__(self, daily_intake, calorie_goal):
        """
        Initialize the CalorieTracker with daily intake and calorie goal.

        :param daily_intake: list of integers representing daily calories consumed
        :param calorie_goal: int representing total calorie goal for the period
        """
        self.daily_intake = daily_intake
        self.calorie_goal = calorie_goal

    def get_total_calories(self):
        """
        Calculate and return the total calories consumed.

        :return: int
        """
        return sum(self.daily_intake)

    def get_goal_status(self):
        """
        Check whether the calorie goal was met.

        :return: str - "Goal Met" if total >= goal, else "Goal Missed"
        """
        total = self.get_total_calories()
        if total >= self.calorie_goal:
            return "Goal Met"
        else:
            return "Goal Missed"
        

