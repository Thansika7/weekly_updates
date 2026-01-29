from abc import ABC, abstractmethod
class CalculatorBase(ABC):

    @abstractmethod
    def calculate(self, a, b):
        pass


class Addition(CalculatorBase):
    def calculate(self, a, b):
        return a + b


class Subtraction(CalculatorBase):
    def calculate(self, a, b):
        return a - b


class Multiplication(CalculatorBase):
    def calculate(self, a, b):
        return a * b


class Division(CalculatorBase):
    def calculate(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    
class Squareroot(CalculatorBase):
    def calculate(self, a, b=None):
        if a < 0:
            raise ValueError("Cannot compute square root of negative number")
        return a ** 0.5
    
class power(CalculatorBase):
    def calculate(self, a, b):
        return a ** b
    
class Remainder(CalculatorBase):
    def calculate(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a % b    

class Calculator:

    def __init__(self):
        self.operations = {
            "1": Addition(),
            "2": Subtraction(),
            "3": Multiplication(),
            "4": Division(),
            "5": Squareroot(),
            "6": power(),
            "7": Remainder()
                    }

    def start(self):
        while True:
            print("\n--- Advanced OOP Calculator ---")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("5. Square Root")
            print("6. Power")
            print("7. Remainder")
            print("8. Exit")
            

            choice = input("Enter your choice (1-8): ")

            if choice == "8":
                print("Calculator closed.")
                break

            try:
                if choice not in self.operations:
                    raise ValueError("Invalid menu choice")

                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))

                operation = self.operations[choice]
                result = operation.calculate(a, b)

                print("Result:", result)

            except ValueError as ve:
                print("Input Error:", ve)

            except ZeroDivisionError as zde:
                print("Math Error:", zde)

            except Exception as e:
                print("Unexpected Error:", e)

            finally:
                print("Operation completed.")


calc = Calculator()
calc.start()
