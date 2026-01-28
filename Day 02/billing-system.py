item=input("Enter the item name: ")
quantity=int(input("Enter the quantity: "))
price=float(input("Enter the price per item: "))

total_cost=quantity*price

print(f"Item: {item}")
print(f"Quantity: {quantity}")
print(f"Total cost: Rs {total_cost}")

print("Total cost for",quantity,item,"is: Rs",total_cost)