from employee_service import (
    add_employee,
    list_employees,
    find_employee,
    update_employee,    
    delete_employee
)


def main():

    while True:

        print("\n================================")
        print("    EMPLOYEE MANAGEMENT SYSTEM")

        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter your choice: ")

    
        if choice == "1":

            print("\n--- ADD EMPLOYEE ---")

            employee_id = input("Enter Employee ID: ").strip()
            name = input("Enter Full Name: ").strip()
            department = input("Enter Department: ").strip()
            email = input("Enter Email: ").strip()
            joining_date = input("Enter Joining Date (YYYY-MM-DD): ").strip()

            result = add_employee(
                employee_id, name, department, email, joining_date
            )

            print(result)

    
        elif choice == "2":

            list_employees()

        
        elif choice == "3":

            employee_id = input("Enter Employee ID: ").strip()

            employee = find_employee(employee_id)

            if employee:
                print("\nEmployee Found!")
                for key, value in employee.items():
                    print(key, ":", value)
            else:
                print("Employee not found.")

        
        elif choice == "4":

            employee_id = input("Enter Employee ID: ").strip()

            print("Leave a field empty if you don't want to change it.")

            new_department = input("Enter New Department: ").strip()
            new_email = input("Enter New Email: ").strip()

            result = update_employee(
                employee_id,
                new_department or None,
                new_email or None
            )

            print(result)

        
        elif choice == "5":

            employee_id = input("Enter Employee ID: ").strip()

            result = delete_employee(employee_id)

            print(result)

        
        elif choice == "6":

            print("Thank you for using Employee Management System!")
            break

        else:

            print("Invalid choice! Please select 1 to 6.")


main()
