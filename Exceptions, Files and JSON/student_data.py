import csv
import os


class StudentData:
    def __init__(self, csv_file="Students.csv"):
        self.csv_file = csv_file
        self.students = []
        self.load_students()

    def load_students(self):
        if os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        row.setdefault('Attendance_Days', '0')
                        row.setdefault('Total_Days', '0')
                        row.setdefault('Absent_Days', '0')
                        self.students.append(row)
                print(f"Loaded {len(self.students)} students")
            except Exception as e:
                print(f"Error loading students: {e}")

    def save_students(self):
        if not self.students:
            print("No students to save")
            return

        try:
            fieldnames = [
                'SID', 'Name', 'Phone', 'Email', 'Address',
                'Branch', 'DOB', 'Enrollment_Date', 'Semester',
                'Attendance_Days', 'Total_Days', 'Absent_Days'
            ]

            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.students)

            print("Students data saved successfully")

        except Exception as e:
            print(f"Error saving students: {e}")

    def add_student(self, sid, name, phone, email, address, branch, dob, enrollment_date, semester='1'):
        for student in self.students:
            if student['SID'] == sid:
                print(f"Student {sid} already exists!")
                return False

        new_student = {
            'SID': sid,
            'Name': name,
            'Phone': phone,
            'Email': email,
            'Address': address,
            'Branch': branch,
            'DOB': dob,
            'Enrollment_Date': enrollment_date,
            'Semester': semester,
            'Attendance_Days': '0',
            'Total_Days': '0',
            "Absent_Days": '0'
        }

        self.students.append(new_student)
        print(f"Student {name} ({sid}) added successfully!")
        return True

    def find_student(self, sid):
        for student in self.students:
            if student['SID'] == sid:
                return student
        return None

    def delete_student(self, sid):
        for i, student in enumerate(self.students):
            if student['SID'] == sid:
                self.students.pop(i)
                print(f"Student {sid} deleted successfully!")
                return True
        print("Student not found!")
        return False

    def view_student(self, sid):
        student = self.find_student(sid)
        if not student:
            print("Student not found!")
            return

        total = int(student.get('Total_Days', '0'))
        attended = int(student.get('Attendance_Days', '0'))
        student['Absent_Days'] = str(total - attended)

        print("STUDENT DETAILS")
        for key in [
            'SID', 'Name', 'Phone', 'Email', 'Address', 'Branch',
            'DOB', 'Enrollment_Date', 'Semester', 'Attendance_Days',
            'Total_Days', 'Absent_Days'
        ]:
            print(f"{key.replace('_',' '):<20}: {student.get(key,'')}")

