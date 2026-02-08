Name=input("Enter name: ")

S1=int(input("Enter marks in subject 1: "))
S2=int(input("Enter marks in subject 2: "))
S3=int(input("Enter marks in subject 3: "))

Average=(S1+S2+S3)/3

if Average>=90:
    print("Grade : A")
elif Average>=80:
    print("Grade : B")
elif Average>=70:
    print("Grade : C")
else:
    print("Fail")