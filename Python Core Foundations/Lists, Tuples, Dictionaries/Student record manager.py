student={}

def calculate_grade(marks):
    total = sum(marks.values())
    average = total / len(marks)

    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def add_student():
    student_id=input("Enter Student ID: ")
    name=input("Enter Student Name: ")
    

    marks={}
    for subject in ['Math', 'Science', 'English', 'Computer Science']:
        mark=int(input(f"Enter marks for {subject}: "))
        marks[subject]=mark
    grade=calculate_grade(marks)
    
    if student_id in student:
        print("Student ID already exists. Use update option to modify.")
    else:
        student[student_id]={'Name':name, 'Marks':marks, 'Grade':grade}
        print("Student added successfully.")

def view_students():
    if not student:
        print("No student records found.")
        return
    for student_id, details in student.items():
        print(f"ID: {student_id}, Name: {details['Name']}, Marks: {details['Marks']}, Grade: {details['Grade']}")

def update_student():
    if student_id in student:
        name=input("Enter new Student Name: ")
        marks={}
        for subject in ['Math', 'Science', 'English', 'Computer Science']:
            mark=int(input(f"Enter new marks for {subject}: "))
            marks[subject]=mark
        grade=calculate_grade(marks)
        student[student_id]={'Name':name, 'Marks':marks, 'Grade':grade}
        print("Student record updated successfully.")
    else:
        print("Student ID not found.")

def delete_student(student_id):
    if student_id in student:
        del student[student_id]
        print("Student record deleted successfully.")
    else:
        print("Student ID not found.")

    
while True:
    print("\nStudent Record Manager:")
    print("1. Add student")
    print("2. View students")
    print("3. Update student")
    print("4. Delete student")
    print("5. Exit")
    
    choice = input("Choose an option (1-5): ")
    
    if choice == '1':
        add_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        student_id=input("Enter Student ID to update: ")
        update_student(student_id)
    elif choice == '4':
        student_id=input("Enter Student ID to delete: ")
        delete_student(student_id)
    elif choice == '5':
        print("Exiting the student record manager.")
        break
    else:
        print("Invalid choice. Please try again.")