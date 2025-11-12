from employee import Employee

class Payroll:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def calculate_total_payroll(self) -> float:
        return round(sum(emp.get_total_compensation() for emp in self.employees), 2)

    def display_summary(self):
        print("=== Payroll Summary ===")
        for emp in self.employees:
            print(emp)
            print(f"  Annual Bonus: {emp.get_annual_bonus()}")
            print(f"  Total Compensation: {emp.get_total_compensation()}")
        print(f"\nTotal Payroll: {self.calculate_total_payroll()}")