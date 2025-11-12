from calorie_tracker import CalorieTracker

if __name__ == "__main__":
    tracker = CalorieTracker([1800, 2000, 2200, 1500], 7000)
    print("Total Calories:", tracker.get_total_calories())   # 7500
    print("Goal Status:", tracker.get_goal_status())         # Goal Met


#expected output
#Total Calories: 7500
# Goal Status: Goal Met