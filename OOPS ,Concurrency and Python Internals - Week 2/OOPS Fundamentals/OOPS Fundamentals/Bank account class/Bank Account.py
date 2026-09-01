import csv  

class AccountHolder:
    def __init__(self, name, account_number,balance=0,pin=None):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.pin = pin

    def deposit(self, amount,pin):
        if self.pin == pin:
            if amount > 0:
                self.balance += amount
                return f"Deposited {amount}. New balance is {self.balance}."
            else:
                return "Deposit amount must be positive."
        else:
            return "Incorrect PIN."
        
    def withdraw(self, amount,pin):
        if self.pin == pin:
            if 0 < amount <= self.balance:
                self.balance -= amount
                return f"Withdrew {amount}. New balance is {self.balance}."
            else:
                return "Insufficient Balance."
        else:
            return "Incorrect PIN."

    def get_balance(self,pin):
        if self.pin == pin:
            return self.balance
        else:
            return "Incorrect PIN."
    
    def transaction(self, target_account, amount, pin):
        if self.pin == pin:
            if 0 < amount <= self.balance:
                self.balance -= amount  
                target_account.balance += amount          
                return f"Transferred {amount} to account {target_account.account_number}. New balance is {self.balance}."
            elif amount==0:
                return "Atleast 1 rupee must be transferred."
        else:
            return "Incorrect PIN."
    
    def transcation_limits(self, amount):
        if amount > 10000:
            return "You can only transfer up to 10,000 at a time."
    
    def get_account_details(self):
        return f"Account Number: {self.account_number}, Name: {self.name}, Balance: {self.balance}" 

    def check_pin(self, entered_pin):
        return self.pin == entered_pin

    def change_pin(self, old_pin, new_pin):
        if self.pin == old_pin:
            self.pin = new_pin
            return "PIN changed successfully."
        else:
            return "Incorrect old PIN." 
    
    
class BankManager:
    def __init__(self, name="Manager"):
        self.name = name
        self.accounts = {}
        self.load_accounts_from_csv()

    def load_accounts_from_csv(self, filename=r"Bank account class/accounts.csv"):
        try:
            with open(filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    account = AccountHolder(
                        name=row["Name"],
                        account_number=row["Account Number"],
                        balance=float(row["Balance"]),
                        pin=int(row["PIN"])
                    )
                    self.accounts[row["Account Number"]] = account
        except FileNotFoundError:
            pass  


    def create_account(self, account_number, name, pin=12345, filename="Bank account class/accounts.csv"):
        if account_number not in self.accounts:
            new_account = AccountHolder(name, account_number, pin=pin)
            self.accounts[account_number] = new_account
            self.save_accounts_to_csv(filename)
            return f"Account created for {name} with account number {account_number}."
        else:
            return "Account already exists."

    def View_account_details(self, account_number):
        account = self.accounts.get(account_number)
        if account:
            return account.get_account_details()
        else:
            return "Account not found."
    
    
    def loan_approval(self, account_number, name ,amount):
        account = self.accounts.get(account_number)
        if account and account.balance >= amount / 2:
            return f"Loan of {amount} approved for account {account_number}."
        else:
            return f"Loan of {amount} denied for account {account_number}."
        
    def save_accounts_to_csv(self, filename="Bank account class/accounts.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account Number", "Name", "Balance", "PIN"])
            for account in self.accounts.values():
                writer.writerow([account.account_number, account.name, account.balance, account.pin])
        return f"All accounts saved."

def main():
    manager= BankManager()
    
    while True:
        print("\nLogin as:")
        print("1. Bank Manager")
        print("2. Account Holder")
        print("3. Exit")
        roll = input("Enter choice: ")

        if roll == '1':
            name=input("Enter Your Name: ")
            print("Logged in as Bank Manager.")

            while True:
                print("1. Create Account")
                print("2. Approve Loan")
                print("3. View User Account Details")
                print("4. Logout")

                choice=input("Enter choice: ")

                if choice == '1':
                    account_number=input("Enter Account Number: ")
                    account_holder_name=input("Enter Account Holder Name: ")
                    name=account_holder_name 
                    pin=12345                   
                    print(manager.create_account(account_number, name, pin=pin))
                
                if choice == '2':
                    account_number=input("Enter Account Number for Loan Approval: ")
                    amount=int(input("Enter Loan Amount: "))
                    print(manager.loan_approval(account_number, name, amount))
                
                if choice == '3':
                    account_number=input("Enter Account Number to View Details: ")               
                    account = manager.View_account_details(account_number)
                    print(account) 

                if choice == '4':
                    print("Logged out.")
                    print(manager.save_accounts_to_csv())
                    break

        elif roll == '2':
            account_number=input("Enter Your Account Number: ")
            account = manager.accounts.get(account_number)
            if not account:
                print("Account not found. Please contact Bank Manager to create an account.")
                continue
            print(f"Logged in as Account Holder")

            while True:
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Transfer Money")
                print("5. View Account Details")
                print("6. Change PIN")
                print("7. Logout")

                choice=input("Enter choice: ")

                if choice == '1':
                    amount=int(input("Enter amount to deposit: "))
                    pin=int(input("Enter your PIN to confirm deposit: "))
                    print(account.deposit(amount, pin))

                if choice == '2':
                    amount=int(input("Enter amount to withdraw: "))
                    pin=int(input("Enter your PIN to confirm withdrawal: "))
                    print(account.withdraw(amount, pin))

                if choice == '3':
                    pin=int(input("Enter your PIN to check balance: "))
                    
                    if account and account.check_pin(pin):
                        print(f"Current Balance: {account.get_balance(pin)}")
                    else:
                        print("Incorrect PIN ")

                if choice == '4':
                    target_account_number=input("Enter Target Account Number: ")
                    target_account = manager.accounts.get(target_account_number)
                    pin=int(input("Enter your PIN to confirm transfer: "))
                    if not account.check_pin(pin):
                        print("Incorrect PIN ")
                        continue
                    if not target_account:
                        print("Target account not found.")
                        continue
                    amount=int(input("Enter amount to transfer: "))
                    limit_msg = account.transcation_limits(amount)
                    if limit_msg:
                        print(limit_msg)
                    else:
                        print(account.transaction(target_account, amount, pin ))
                if choice == '5':
                    if account:
                        print(account.get_account_details())

                if choice == '6':
                    old_pin = int(input("Enter old PIN: "))
                    new_pin = int(input("Enter new PIN: "))
                    print(account.change_pin(old_pin, new_pin))

                if choice == '7':
                    print("Logged out.")
                    print(manager.save_accounts_to_csv())
                    break   
        elif roll == '3':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()       


        



