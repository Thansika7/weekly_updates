class AttendanceManagement:
    def __init__(self, student_data):
        self.student_data = student_data

    def mark_attendance(self, sid, present=True):
        student = self.student_data.find_student(sid)
        if not student:
            print("Student not found!")
            return False

        total_days = int(student.get('Total_Days', '0')) + 1
        student['Total_Days'] = str(total_days)

        if present:
            attendance_days = int(student.get('Attendance_Days', '0')) + 1
            student['Attendance_Days'] = str(attendance_days)

        student['Absent_Days'] = str(int(student['Total_Days']) - int(student['Attendance_Days']))

        print(f"Attendance updated for {student['Name']} ({sid})")
        self.student_data.save_students()
        return True

    def view_attendance_info(self, sid):
        student = self.student_data.find_student(sid)
        if not student:
            print("Student not found!")
            return None

        attended = int(student.get('Attendance_Days', '0'))
        total = int(student.get('Total_Days', '0'))
        absent = total - attended
        percentage = (attended / total * 100) if total > 0 else 0

        print("\nATTENDANCE DETAILS")
        print(f"Attended Days : {attended}")
        print(f"Total Days    : {total}")
        print(f"Absent Days   : {absent}")
        print(f"Percentage    : {percentage:.2f}%")

        return percentage
