from datetime import datetime
students_details={date:{'id':[], 'name':[], 'status':[]} for date in []}
holidays = [] 
def is_weekend(date_str):
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    return date_obj.weekday() >= 5 

def holiday_dates():
    global holidays
    n = int(input("Enter number of holidays to add: "))
    for i in range(n):
        holiday = input("Enter holiday date (DD-MM-YYYY): ")
        holidays.append(holiday)
    print(f"Holidays added: {holidays}")

def Staff_portal():
    print("Staff portal")
    while True:
        print("1. Enter Holidays")
        print("2. Mark Attendance")
        print("3. View Attendance Report")
        print("4. Update Student Attendance")
        print("5. Holiday Dates")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            holiday_dates()
        elif choice == '2':
            mark_attendance()
        elif choice == '3':
            view_attendance_report()
        elif choice == '4':
            update_student_attendance()
        elif choice == '5':
            holiday_dates()
        elif choice == '6':
            print("Logged out successfully.")
        else:
            print("Invalid choice. Please try again.")

def mark_attendance():
    date = input("Enter the date (DD-MM-YYYY): ")
    if is_weekend(date):
        print("It's a weekend. Cannot mark attendance.")
        return
    if date in holidays:
        print("It's a holiday. Cannot mark attendance.")
        return
    if date not in students_details and date not in holidays:
        students_details[date] = {'id': [], 'name': [], 'status': []}
    print("Marking attendance for students on", date)
    x = int(input("Enter number of students: "))
    for i in range(x):
        student_id = input("Enter student ID: ")
        student_name = input("Enter student name: ")
        status = input("Enter attendance status (P/A): ").upper()
        students_details[date]['id'].append(student_id)
        students_details[date]['name'].append(student_name)
        students_details[date]['status'].append(status)
    print("Attendance marked successfully.")

def view_attendance_report():
    print("Attendance Report")
    student_id = input("Enter Student ID to view report: ")    
    found = False
    present_count = 0
    total_count = 0
    student_name = ""
    
    for date, details in students_details.items():
        if student_id in details['id']:
            index = details['id'].index(student_id)
            print(f"Date: {date}, Name: {details['name'][index]}, Status: {details['status'][index]}")
            student_name = details['name'][index]
            total_count += 1
            if details['status'][index] == 'P':
                present_count += 1
            found = True
    
    if found:
        percentage = (present_count / total_count) * 100 if total_count > 0 else 0
        print(f"\n--- Attendance Summary ---")
        print(f"Student ID: {student_id}")
        print(f"Name: {student_name}")
        print(f"Total Classes: {total_count}")
        print(f"Present: {present_count}")
        print(f"Absent: {total_count - present_count}")
        print(f"Attendance Percentage: {percentage:.2f}%")
    else:
        print(f"No attendance records found for Student ID: {student_id}")
        

def update_student_attendance():
    date = input("Enter the date (DD-MM-YYYY) to update attendance: ")
    if date in students_details and date not in holidays:
        student_id = input("Enter student ID to update: ")
        if student_id in students_details[date]['id']:
            index = students_details[date]['id'].index(student_id)
            new_status = input("Enter new attendance status (P/A): ").upper()
            students_details[date]['status'][index] = new_status
            print("Attendance updated successfully.")
        else:
            print("Student ID not found for the given date.")
    else:
        print("No attendance record found for the given date.")

def Student_portal():
    print("Student Portal")
    student_id = input("Enter your Student ID: ")
    found = False
    for date, details in students_details.items():
        if student_id in details['id']:
            found = True
            index = details['id'].index(student_id)
            print(f"Date: {date}, Name: {details['name'][index]}, Status: {details['status'][index]}")
    if not found:
        print("No attendance records found for the given Student ID.")

def main():
    while True:
        print("1. Staff Portal")
        print("2. Student Portal")
        print("3. Log out")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            Staff_portal()
        elif choice == '2':
            Student_portal()
        elif choice == '3':
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
