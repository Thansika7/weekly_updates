import random

def number_guessing_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    max_attempts = int(input("Enter the number of attempts you want: "))
    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please guess a number within the range of 1 to 100.")
                continue

            if guess < number_to_guess:
                print("Too low!")
            elif guess > number_to_guess:
                print("Too high!")
            else:
                print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if attempts == max_attempts:
        print(f"Sorry, you've used all your attempts. The number was {number_to_guess}.")

number_guessing_game() 