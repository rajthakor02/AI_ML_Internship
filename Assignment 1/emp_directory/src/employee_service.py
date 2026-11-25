
import json
import re
from pathlib import Path
from datetime import datetime



BASE_DIR = Path(__file__).resolve().parent.parent


DATA_FILE = BASE_DIR / "data" / "employees.json"



def load_employees():

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        save_employees([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            employees = json.load(file)

        if not isinstance(employees, list):
            raise ValueError("Employee data must be a list.")

        return employees

    except json.JSONDecodeError:
        raise ValueError("Employee JSON file is corrupted.")

def save_employees(employees):

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)



def validate_employee(employee_id, name, department, email, joining_date):

    if not all([employee_id, name, department, email, joining_date]):
        return "All fields are required."

    if not re.fullmatch(r"[A-Za-z0-9_-]+", employee_id):
        return "Invalid employee ID."

    email_pattern = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(email_pattern, email):
        return "Invalid email address."

    try:
        datetime.strptime(joining_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date. Use YYYY-MM-DD."

    return None


def add_employee(employee_id, name, department, email, joining_date):

    employees = load_employees()

    
    for employee in employees:
        if employee["employee_id"] == employee_id:
            return "Employee ID already exists!"

    
    error = validate_employee(
        employee_id, name, department, email, joining_date
    )

    if error:
        return error


    new_employee = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "email": email,
        "joining_date": joining_date
    }

    employees.append(new_employee)

    save_employees(employees)

    return "Employee added successfully!"



def list_employees():

    employees = load_employees()

    if not employees:
        print("No employees found.")
        return

    print("\n========== EMPLOYEE LIST ==========")

    for employee in employees:

        print("--------------------------------")
        print("Employee ID:", employee["employee_id"])
        print("Name:", employee["name"])
        print("Department:", employee["department"])
        print("Email:", employee["email"])
        print("Joining Date:", employee["joining_date"])


def find_employee(employee_id):

    employees = load_employees()

    for employee in employees:

        if employee["employee_id"] == employee_id:
            return employee

    return None



def update_employee(employee_id, new_department=None, new_email=None):

    employees = load_employees()

    for employee in employees:

        if employee["employee_id"] == employee_id:

            if new_department:
                employee["department"] = new_department

            if new_email:
                if not re.fullmatch(
                    r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$", new_email
                ):
                    return "Invalid email address."

                employee["email"] = new_email

            save_employees(employees)

            return "Employee updated successfully!"

    return "Employee not found."



def delete_employee(employee_id):

    employees = load_employees()

    for employee in employees:

        if employee["employee_id"] == employee_id:

            confirmation = input(
                "Are you sure you want to delete this employee? (yes/no): "
            )

            if confirmation.lower() == "yes":

                employees.remove(employee)
                save_employees(employees)

                return "Employee deleted successfully!"

            return "Deletion cancelled."

    return "Employee not found."
