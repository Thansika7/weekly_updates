class SearchFilter:
    def __init__(self, student_data):
        self.student_data = student_data

    def search_by_name(self, name):
        results = []
        for student in self.student_data.students:
            if name.lower() in student['Name'].lower():
                results.append(student)

        self.display_results(results, f"Search results for name: {name}")
        return results

    def search_by_sid(self, sid):
        results = []
        for student in self.student_data.students:
            if sid.lower() in student['SID'].lower():
                results.append(student)

        self.display_results(results, f"Search results for SID: {sid}")
        return results

    def filter_by_branch(self, branch):
        results = []
        for student in self.student_data.students:
            if student['Branch'].lower() == branch.lower():
                results.append(student)

        self.display_results(results, f"Students in {branch}")
        return results

    def filter_by_semester(self, semester):
        results = []
        for student in self.student_data.students:
            if student['Semester'] == semester:
                results.append(student)

        self.display_results(results, f"Students in Semester {semester}")
        return results

    def filter_by_attendance(self, min_percentage):
        results = []
        for student in self.student_data.students:
            try:
                total_days = int(student['Total_Days'])
                attended_days = int(student['Attendance_Days'])
                if total_days > 0 and (attended_days / total_days) * 100 >= float(min_percentage):
                    results.append(student)
            except:
                pass

        self.display_results(results, f"Students with {min_percentage}% or higher attendance")
        return results

    def display_results(self, results, title):
        if len(results) == 0:
            print(f"\n{title}: No results found.\n")
            return

        print(f"\n{title}: {len(results)} found")
        print(f"{'SID':<10} {'Name':<20} {'Branch':<15} {'Semester':<10} {'Attendance':<15}")

        for student in results:
            try:
                total = int(student['Total_Days'])
                attended = int(student['Attendance_Days'])
                if total > 0:
                    attendance = (attended / total) * 100
                    attendance_str = f"{attendance:.2f}%"
                else:
                    attendance_str = "N/A"
            except:
                attendance_str = "N/A"

            print(f"{student['SID']:<10} {student['Name']:<20} {student['Branch']:<15} {student['Semester']:<10} {attendance_str:<15}")

