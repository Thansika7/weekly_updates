cart={}

def add_item(item, quantity):
    if item in cart:
        cart[item] += quantity
    else:
        cart[item] = quantity
    print(f"Added {quantity} {item} to the cart.")

def view_cart():
    if not cart:
        print("Your cart is empty.")
    else:
        print("Your cart contains:")
        for item, quantity in cart.items():
            print(f"{item}: {quantity}")

def update_item(item, quantity):
    if item in cart:
        cart[item] = quantity
        print(f"Updated {item} to {quantity}.")
    else:
        print(f"{item} is not in the cart.")

def delete_item(item):
    if item in cart:
        del cart[item]
        print(f"Deleted {item} from the cart.")
    else:
        print(f"{item} is not in the cart.")

while True:
    print("\nShopping Cart Menu:")
    print("1. Add item")
    print("2. View cart")
    print("3. Update item")
    print("4. Delete item")
    print("5. Exit")
    
    choice = input("Choose an option (1-5): ")
    
    if choice == '1':
        item = input("Enter item name: ").lower()
        quantity = int(input("Enter quantity: "))
        add_item(item, quantity)
    elif choice == '2':
        view_cart()
    elif choice == '3':
        item = input("Enter item name to update: ").lower()
        quantity = int(input("Enter new quantity: "))
        update_item(item, quantity)
    elif choice == '4':
        item = input("Enter item name to delete: ").lower()
        delete_item(item)
    elif choice == '5':
        print("Exiting the shopping cart system.")
        break
    else:
        print("Invalid choice. Please try again.")
