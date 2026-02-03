from user_management import UserManagement
from student_data import StudentData
from attendance import AttendanceManagement
from search_filter import SearchFilter
from reports import Reports


class StudentManagementPortal:

    def __init__(self):
        self.user_mgmt = UserManagement()
        self.student_data = StudentData()
        self.attendance = AttendanceManagement(self.student_data)
        self.search = SearchFilter(self.student_data)
        self.reports = Reports(self.student_data)

    def display_login_menu(self):
        print("\nSTUDENT MANAGEMENT SYSTEM")
        print("1. Login")
        print("2. Exit")

    def display_main_menu(self):
        user = self.user_mgmt.current_user
        print(f"\nLogged in as: {user.username} ({user.role})")

        if user.role == 'faculty':
            print("\n--- STUDENT MANAGEMENT ---")
            print("1. Add Student")
            print("2. View Student Details")
            print("3. Delete Student")

            print("\n--- ATTENDANCE ---")
            print("4. Mark Attendance")
            print("5. View Attendance")

            print("\n--- SEARCH ---")
            print("6. Search by Name")
            print("7. Search by Student ID")
            print("8. Filter by Branch")
            print("9. Filter by Semester")
            print("10. Filter by Attendance %")

            print("\n--- REPORTS ---")
            print("11. Attendance Report")

            print("\n--- USER MANAGEMENT ---")
            print("12. Register New User")

            print("13. Logout")
            print("14. Exit")

        else:
            print("\n--- STUDENT MENU ---")
            print("1. View My Details")
            print("2. View My Attendance")
            print("3. Logout")
            print("4. Exit")

    def run(self):
        while True:

            if self.user_mgmt.current_user is None:
                self.display_login_menu()
                choice = input("Enter choice: ").strip()

                if choice == '1':
                    self.user_mgmt.login(
                        input("Username: "),
                        input("Password: ")
                    )
                elif choice == '2':
                    print("Exiting system...")
                    break
                else:
                    print("Invalid choice!")

            else:
                self.display_main_menu()
                choice = input("Enter choice: ").strip()
                user = self.user_mgmt.current_user

                if user.role == 'faculty':

                    if choice == '1':
                        sid = input("Student ID: ")
                        name = input("Name: ")
                        phone = input("Phone: ")
                        email = input("Email: ")
                        address = input("Address: ")
                        branch = input("Branch: ")
                        dob = input("DOB: ")
                        enroll = input("Enrollment Date: ")
                        semester = input("Semester: ")

                        self.student_data.add_student(
                            sid, name, phone, email,
                            address, branch, dob, enroll, semester
                        )
                        self.student_data.save_students()

                    elif choice == '2':
                        self.student_data.view_student(
                            input("Enter Student ID: ")
                        )

                    elif choice == '3':
                        self.student_data.delete_student(
                            input("Enter Student ID: ")
                        )
                        self.student_data.save_students()

                    elif choice == '4':
                        sid = input("Student ID: ")
                        status = input("P = Present / A = Absent: ").lower()
                        if status in ['p', 'a']:
                            self.attendance.mark_attendance(sid, status == 'p')
                            self.student_data.save_students()
                        else:
                            print("Invalid input!")

                    elif choice == '5':
                        self.attendance.view_attendance_info(
                            input("Enter Student ID: ")
                        )

                    elif choice == '6':
                        self.search.search_by_name(input("Enter name: "))

                    elif choice == '7':
                        self.search.search_by_sid(input("Enter Student ID: "))

                    elif choice == '8':
                        self.search.filter_by_branch(input("Enter branch: "))

                    elif choice == '9':
                        self.search.filter_by_semester(input("Enter semester: "))

                    elif choice == '10':
                        self.search.filter_by_attendance(
                            input("Minimum attendance %: ")
                        )

                    elif choice == '11':
                        self.reports.generate_attendance_report()

                    elif choice == '12':
                        username = input("New username: ")
                        password = input("Password: ")
                        role = input("Role (faculty/student): ").lower()

                        if role not in ['faculty', 'student']:
                            print("Invalid role!")
                        else:
                            self.user_mgmt.register_user(username, password, role)

                    elif choice == '13':
                        self.user_mgmt.logout()

                    elif choice == '141':
                        print("Exited")
                        break

                    else:
                        print("Invalid choice!")

                else:

                    if choice == '1':
                        sid = input("Enter your Student ID: ")
                        self.student_data.view_student(sid)

                    elif choice == '2':
                        sid = input("Enter your Student ID: ")
                        self.attendance.view_attendance_info(sid)

                    elif choice == '3':  
                        self.user_mgmt.logout()

                    elif choice == '4':  
                        print("Exited")
                        break

                    else:
                        print("Invalid choice!")


if __name__ == "__main__":
    StudentManagementPortal().run()
