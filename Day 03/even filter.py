numbers=input("Enter numbers: ").split()
even_numbers=[]
odd_numbers=[]
for num in numbers:
    if int(num)%2==0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

print("Even numbers:", even_numbers)
print("Odd numbers:", odd_numbers)