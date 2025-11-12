from employee import Employee
from payroll import Payroll

if __name__ == "__main__":
    e1 = Employee("E101", "Alice", 5000, 10)
    e2 = Employee("E102", "Bob", 7000, 12)

    manager = Payroll()
    manager.add_employee(e1)
    manager.add_employee(e2)

    manager.display_summary()