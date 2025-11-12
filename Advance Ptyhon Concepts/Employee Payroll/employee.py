class Employee:
    def __init__(self, empID: str, name: str, monthly_salary: int, bonus_rate: float):
        self.empID = empID
        self.name = name
        self.monthly_salary = monthly_salary
        self.bonus_rate = bonus_rate

    def get_annual_bonus(self) -> float:
        return round((self.monthly_salary * 12 * self.bonus_rate) / 100, 2)

    def get_total_compensation(self) -> float:
        return round((self.monthly_salary * 12) + self.get_annual_bonus(), 2)

    def __str__(self):
        return f"Employee[ID: {self.empID}, Name: {self.name}]"