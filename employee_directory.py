
import json
import os

FILE_NAME = "employees.json"


# Load employee data from JSON file
def load_employees():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


# Save employee data into JSON file
def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


# Add a new employee
def add_employee():
    employees = load_employees()

    employee_id = input("Enter Employee ID: ")

    # Check duplicate employee ID
    for employee in employees:
        if employee["employee_id"] == employee_id:
            print("Employee ID already exists!")
            return

    name = input("Enter Employee Name: ")
    department = input("Enter Department: ")
    email = input("Enter Email: ")
    joining_date = input("Enter Joining Date (YYYY-MM-DD): ")

    if not all([employee_id, name, department, email, joining_date]):
        print("All fields are required!")
        return

    new_employee = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "email": email,
        "joining_date": joining_date
    }

    employees.append(new_employee)
    save_employees(employees)

    print("Employee added successfully!")


# Display all employees
def view_employees():
    employees = load_employees()

    if not employees:
        print("No employees found!")
        return

    print("\n----- Employee List -----")

    for employee in employees:
        print("ID:", employee["employee_id"])
        print("Name:", employee["name"])
        print("Department:", employee["department"])
        print("Email:", employee["email"])
        print("Joining Date:", employee["joining_date"])
        print("------------------------")


# Search employee
def search_employee():
    employees = load_employees()
    employee_id = input("Enter Employee ID to search: ")

    for employee in employees:
        if employee["employee_id"] == employee_id:
            print("\nEmployee Found!")
            print(employee)
            return

    print("Employee not found!")


# Update employee
def update_employee():
    employees = load_employees()
    employee_id = input("Enter Employee ID to update: ")

    for employee in employees:
        if employee["employee_id"] == employee_id:

            print("Leave blank if you don't want to change a field.")

            name = input("Enter new name: ")
            department = input("Enter new department: ")
            email = input("Enter new email: ")

            if name:
                employee["name"] = name

            if department:
                employee["department"] = department

            if email:
                employee["email"] = email

            save_employees(employees)
            print("Employee updated successfully!")
            return

    print("Employee not found!")


# Delete employee
def delete_employee():
    employees = load_employees()
    employee_id = input("Enter Employee ID to delete: ")

    for employee in employees:
        if employee["employee_id"] == employee_id:

            confirmation = input("Are you sure? (yes/no): ")

            if confirmation.lower() == "yes":
                employees.remove(employee)
                save_employees(employees)
                print("Employee deleted successfully!")
            else:
                print("Deletion cancelled!")

            return

    print("Employee not found!")


# Main menu
while True:

    print("\n===== EMPLOYEE DIRECTORY =====")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        print("Thank you for using Employee Directory!")
        break

    else:
        print("Invalid choice! Please try again.")
