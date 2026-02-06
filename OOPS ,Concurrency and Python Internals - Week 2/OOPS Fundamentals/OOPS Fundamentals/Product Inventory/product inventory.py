import csv

class ProductInventory:
    def __init__(self):
        self.inventory = {}
        self.load_products_from_csv()
    
    def load_products_from_csv(self, filename=r"Product Inventory/products.csv"):
        try:
            with open(filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.inventory[row["Product ID"]] = {
                        "name": row["Name"],
                        "quantity": int(row["Quantity"])
                    }
        except FileNotFoundError:
            pass   


    def add_product(self, product_id, name, quantity, filename="Product Inventory\products.csv"):
        if product_id in self.inventory:
            self.inventory[product_id]['quantity'] += quantity
        else:
            self.inventory[product_id] = {'name': name, 'quantity': quantity}
        self.save_products_to_csv(filename)
    
    def update_product_quantity(self, product_id, new_quantity, filename="Product Inventory\products.csv"):
        if product_id in self.inventory:
            self.inventory[product_id]['quantity'] = new_quantity
            self.save_products_to_csv(filename)
        else:
            raise KeyError("Product not found in inventory")

    def remove_product(self, product_id, quantity):
        if product_id in self.inventory:
            if self.inventory[product_id]['quantity'] >= quantity:
                self.inventory[product_id]['quantity'] -= quantity
                if self.inventory[product_id]['quantity'] == 0:
                    del self.inventory[product_id]
            else:
                raise ValueError("Not enough quantity to remove")
        else:
            raise KeyError("Product not found in inventory")

    def get_product_info(self, product_id):
        if product_id in self.inventory:
            return self.inventory[product_id]
        else:
            raise KeyError("Product not found in inventory")

    def list_inventory(self):
        return self.inventory
    
    def save_products_to_csv(self, filename="Product Inventory\products.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Product ID", "Name", "Quantity"])
            for product_id, info in self.inventory.items():
                writer.writerow([product_id, info['name'], info['quantity']])
        return f"All products saved."

def main():
    inventory= ProductInventory()

    while True:

        print("\nProduct Inventory Management:")
        print("1. Add Product")
        print("2. Remove Product")  
        print("3. Update Product")    
        print("4. Get Product Info")
        print("5. List Inventory") 
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            quantity = int(input("Enter Quantity: "))
            inventory.add_product(product_id, name, quantity)
            print(f"Product {name} added successfully.")

        elif choice == "2":
            product_id = input("Enter Product ID: ")
            quantity = int(input("Enter Quantity to Remove: "))
            if product_id in inventory.list_inventory():
                inventory.remove_product(product_id, quantity)
                print(f"Product {product_id} removed successfully.")
            else:
                print("Product not found in inventory.")

        elif choice == "3":
            product_id = input("Enter Product ID: ")
            new_quantity = int(input("Enter New Quantity: "))
            try:
                inventory.update_product_quantity(product_id, new_quantity)
                print(f"{product_id} updated successfully.")
            except KeyError as e:
                print(e)

        elif choice == "4":
            product_id = input("Enter Product ID: ")
            try:
                product_info = inventory.get_product_info(product_id)
                print(f"Product Info - ID: {product_id}, Name: {product_info['name']}, Quantity: {product_info['quantity']}")
            except KeyError as e:
                print(e)
        
        elif choice == "5":
            all_products = inventory.list_inventory()
            for pid, info in all_products.items():
                print(f"Product ID: {pid}, Name: {info['name']}, Quantity: {info['quantity']}")

        elif choice == "6":
            print("Exiting Product Inventory Management.")
            print(inventory.save_products_to_csv())
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



        
    
