import math
import sys
import time

def square_root(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        print("Error: Cannot calculate square root of a negative number.")
        return None

def factorial(x):
    if x >= 0 and x == int(x):
        return math.factorial(x)
    else:
        print("Error: Factorial is only defined for non-negative integers.")
        return None

def natural_logarithm(x):
    if x > 0:
        return math.log(x)
    else:
        print("Error: Natural logarithm is only defined for positive numbers.")
        return None

def power(x, b):
    return math.pow(x, b)

def display_menu():
    print("\nScientific Calculator Menu:")
    print("1. Square Root (√x)")
    print("2. Factorial (x!)")
    print("3. Natural Logarithm (ln(x))")
    print("4. Power (x^b)")
    print("5. Exit")

def interactive_mode():
    while True:
        display_menu()
        try:
            choice = input("Enter your choice (1-5): ")
        except EOFError:
            print("Invalid Input")
            continue
        if choice == '1':
            try:
                x = float(input("Enter the number (x): "))
                result = square_root(x)
                if result is not None:
                    print(f"Square root of {x} is: {result}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '2':
            try:
                x = int(input("Enter the number (x): "))
                result = factorial(x)
                if result is not None:
                    print(f"Factorial of {x} is: {result}")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif choice == '3':
            try:
                x = float(input("Enter the number (x): "))
                result = natural_logarithm(x)
                if result is not None:
                    print(f"Natural logarithm of {x} is: {result}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '4':
            try:
                x = float(input("Enter the base (x): "))
                b = float(input("Enter the exponent (b): "))
                result = power(x, b)
                print(f"{x} raised to the power of {b} is: {result}")
            except ValueError:
                print("Invalid input. Please enter numbers.")
        elif choice == '5':
            print("Exiting the calculator...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def main():
    if sys.stdin.isatty():
        print("Running interactively...")
        interactive_mode()
    else:
        print("Running Non-interactively")
        while True:
            time.sleep(10)  # Keeps the container running

if __name__ == "__main__":
    main()