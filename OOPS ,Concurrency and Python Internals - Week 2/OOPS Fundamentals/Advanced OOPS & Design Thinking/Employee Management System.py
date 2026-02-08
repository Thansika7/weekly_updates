import json
import os
from abc import ABC, abstractmethod

EMP_FILE = "employees.json"
USER_FILE = "users.json"

class LeaveActions(ABC):

    @abstractmethod
    def view_leave_requests(self):
        pass

    @abstractmethod
    def process_leave(self, emp_id, approve, role):
        pass


class Admin(LeaveActions):

    def __init__(self):
        self.employees = {}
        self.load_employees()

    def load_employees(self):
        if os.path.exists(EMP_FILE):
            try:
                with open(EMP_FILE, "r") as f:
                    content = f.read().strip()
                    if content:
                        self.employees = json.loads(content)
                    else:
                        self.employees = {}
            except json.JSONDecodeError:
                print("Warning: employees.json corrupted. Initializing empty data.")
                self.employees = {}
        else:
            self.employees = {}

    def save_employees(self):
        with open(EMP_FILE, "w") as f:
            json.dump(self.employees, f, indent=4)

    def create_employee(self):
        emp_id = input("ID: ")
        self.employees[emp_id] = {
            "Name": input("Name: "),
            "Department": input("Department: "),
            "Position": input("Position: "),
            "Address": input("Address: "),
            "Attendance": {"Total": 0, "Present": 0, "Absent": 0},
            "LeaveStatus": "None",
            "LeaveReason": ""
        }
        self.save_employees()
        print("Employee added")

    def update_employee(self):
        emp_id = input("Employee ID: ")
        if emp_id in self.employees:
            self.employees[emp_id]["Department"] = input("New Department: ")
            self.employees[emp_id]["Position"] = input("New Position: ")
            self.save_employees()
            print("Employee updated")

    def delete_employee(self):
        emp_id = input("Employee ID: ")
        if emp_id in self.employees:
            del self.employees[emp_id]
            self.save_employees()
            print("Employee deleted")

    def view_employee_details(self):
        self.load_employees()
        for emp_id, e in self.employees.items():
            print("-" * 30)
            print("ID:", emp_id)
            print("Name:", e["Name"])
            print("Department:", e["Department"])
            print("Position:", e["Position"])
            print("Address:", e["Address"])
            print("Leave Status:", e["LeaveStatus"])
            att = e["Attendance"]
            print(f"Total Days: {att['Total']}, Present: {att['Present']}, Absent: {att['Absent']}")

    def mark_attendance(self):
        emp_id = input("Employee ID: ")
        if emp_id in self.employees:
            status = input("Present / Absent: ").strip().lower()
            if status not in ["present", "absent"]:
                print("Invalid input! Use 'Present' or 'Absent'.")
                return
            self.employees[emp_id]["Attendance"]["Total"] += 1
            if status == "present":
                self.employees[emp_id]["Attendance"]["Present"] += 1
            else:
                self.employees[emp_id]["Attendance"]["Absent"] += 1
            self.save_employees()
            print("Attendance marked")

    def view_leave_requests(self):
        self.load_employees()
        has_requests = False
        for emp_id, e in self.employees.items():
            if e["LeaveStatus"] == "Pending":
                has_requests = True
                print("-" * 30)
                print("ID:", emp_id)
                print("Name:", e["Name"])
                print("Reason:", e["LeaveReason"])
        if not has_requests:
            print("No pending leave requests.")

    def process_leave(self, emp_id, approve, role):
        if emp_id in self.employees and self.employees[emp_id]["LeaveStatus"] == "Pending":
            self.employees[emp_id]["LeaveStatus"] = "Approved" if approve else "Denied"
            self.employees[emp_id]["LeaveReason"] += f" (By {role})"
            self.save_employees()
            print("Leave processed")
        else:
            print("No pending leave for this employee.")

    def add_user(self):
        users = load_users()
        username = input("Username: ")
        users[username] = {
            "password": input("Password: "),
            "role": input("Role (admin/manager/employee): ")
        }
        save_users(users)
        print("User added")


class Manager(Admin):
    def create_employee(self): pass
    def update_employee(self): pass
    def delete_employee(self): pass
    def mark_attendance(self): pass
    def add_user(self): pass

    def view_employee_details(self):
        self.load_employees()
        for emp_id, e in self.employees.items():
            print("-" * 30)
            print("ID:", emp_id)
            print("Name:", e["Name"])
            print("Department:", e["Department"])
            print("Position:", e["Position"])
            att = e["Attendance"]
            print(f"Total Days: {att['Total']}, Present: {att['Present']}, Absent: {att['Absent']}")
            print("Leave Status:", e["LeaveStatus"])


class Employee(Admin):
    def create_employee(self): pass
    def update_employee(self): pass
    def delete_employee(self): pass
    def mark_attendance(self): pass
    def add_user(self): pass
    def view_employee_details(self): pass

    def view_my_details(self, emp_id):
        if emp_id in self.employees:
            e = self.employees[emp_id]
            print("-" * 30)
            print("ID:", emp_id)
            print("Name:", e["Name"])
            print("Department:", e["Department"])
            print("Position:", e["Position"])
            print("Address:", e["Address"])
            print("Leave Status:", e["LeaveStatus"])
            att = e["Attendance"]
            print(f"Total Days: {att['Total']}, Present: {att['Present']}, Absent: {att['Absent']}")

    def update_address(self, emp_id):
        self.employees[emp_id]["Address"] = input("New Address: ")
        self.save_employees()
        print("Address updated")

    def request_leave(self, emp_id):
        self.employees[emp_id]["LeaveStatus"] = "Pending"
        self.employees[emp_id]["LeaveReason"] = input("Reason: ")
        self.save_employees()
        print("Leave requested")

    def view_leave_status(self, emp_id):
        print("Leave Status:", self.employees[emp_id]["LeaveStatus"])


def load_users():
    if not os.path.exists(USER_FILE):
        save_users({"admin": {"password": "admin123", "role": "admin"}})
    try:
        with open(USER_FILE, "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return {"admin": {"password": "admin123", "role": "admin"}}
    except json.JSONDecodeError:
        print("Warning: users.json corrupted. Initializing default admin user.")
        return {"admin": {"password": "admin123", "role": "admin"}}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def login(users):
    u = input("Username: ")
    p = input("Password: ")
    if u in users and users[u]["password"] == p:
        return users[u]["role"], u
    return None, None


if __name__ == "__main__":
    admin = Admin()
    manager = Manager()
    employee = Employee()
    users = load_users()

    while True:
        print("\n1. Login\n2. Exit")
        choice = input("Choice: ")

        if choice == "1":
            role, username = login(users)
            if not role:
                print("Invalid login")
                continue

            if role == "admin":
                while True:
                    print("""
1. Add Employee
2. Update Employee
3. Delete Employee
4. View Employees
5. Mark Attendance
6. View Leave Requests
7. Process Leave
8. Add User
9. Logout
""")
                    c = input("Choice: ")
                    if c == "1": admin.create_employee()
                    elif c == "2": admin.update_employee()
                    elif c == "3": admin.delete_employee()
                    elif c == "4": admin.view_employee_details()
                    elif c == "5": admin.mark_attendance()
                    elif c == "6": admin.view_leave_requests()
                    elif c == "7":
                        emp_id = input("Employee ID: ")
                        approve = input("Approve? (y/n): ").strip().lower() == "y"
                        admin.process_leave(emp_id, approve, "Admin")
                    elif c == "8": admin.add_user()
                    elif c == "9": break

            elif role == "manager":
                while True:
                    print("\n1. View Employees\n2. View Leave Requests\n3. Process Leave\n4. Logout")
                    c = input("Choice: ")
                    if c == "1": manager.view_employee_details()
                    elif c == "2": manager.view_leave_requests()
                    elif c == "3":
                        emp_id = input("Employee ID: ")
                        approve = input("Approve? (y/n): ").strip().lower() == "y"
                        manager.process_leave(emp_id, approve, "Manager")
                    elif c == "4": break

            elif role == "employee":
                employee.load_employees()  # refresh latest data
                emp_id = input("Enter your Employee ID: ")
                if emp_id not in employee.employees:
                    print("Invalid Employee ID")
                    continue

                while True:
                    print("""
1. View My Details
2. Update Address
3. Request Leave
4. View Leave Status
5. Logout
""")
                    c = input("Choice: ")
                    if c == "1": employee.view_my_details(emp_id)
                    elif c == "2": employee.update_address(emp_id)
                    elif c == "3": employee.request_leave(emp_id)
                    elif c == "4": employee.view_leave_status(emp_id)
                    elif c == "5": break

        elif choice == "2":
            print("Exiting program...")
            break
