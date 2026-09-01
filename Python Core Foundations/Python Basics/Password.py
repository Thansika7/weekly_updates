Password= input("Enter your password: ")
length=len(Password)
digits=False
upper=False
for char in Password:
    if char.isdigit():
        digits=True
    if char.isupper():
        upper=True

if length<8:
    print("Weak Password")  
elif length>=8 and digits and upper:
    print("Strong Password")
else:
    print("Medium Password")