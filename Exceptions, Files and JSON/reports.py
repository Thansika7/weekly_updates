class Reports:
    def __init__(self, student_data):
        self.student_data = student_data

    def generate_attendance_report(self):
        if len(self.student_data.students) == 0:
            print("No students to report")
            return

        print("ATTENDANCE REPORT")
        print(f"{'SID':<10} {'Name':<20} {'Attended':<10} {'Total':<10} {'Absent':<10} {'Percentage':<12}")

        for student in self.student_data.students:
            try:
                attended = int(student.get('Attendance_Days', 0))
                total = int(student.get('Total_Days', 0))
                absent = total - attended

                percentage = (attended / total * 100) if total > 0 else 0

                print(f"{student['SID']:<10} {student['Name']:<20} {attended:<10} {total:<10} {absent:<10} {percentage:>10.2f}%")
            except Exception as e:
                print(f"{student.get('SID','')} {student.get('Name','')} Error in calculation: {e}")
