num1=float(input("Enter first number: "))
num2=float(input("Enter second number: "))

Choise=input("Enter operation (1. Addition, 2. Subtraction, 3. Multiplication, 4. Division): ")

if Choise=='1':
    print(num1,"+",num2,"=",num1+num2)
elif Choise=='2':
    print(num1,"-",num2,"=",num1-num2)
elif Choise=='3':
    print(num1,"*",num2,"=",num1*num2)
elif Choise=='4':
    print(num1,"/",num2,"=",num1/num2)
else:
    print("Invalid input")
