#!/usr/bin/env python3
import random
import sys

class GuessTheNumber:
    def __init__(self):
        self.modes = {
            "easy": {"digits": 4, "attempts": 4},
            "medium": {"digits": 5, "attempts": 5},
            "hard": {"digits": 6, "attempts": 6}
        }
        self.secret_number = None
        self.mode = None
        self.attempts_left = 0
        self.game_over = False

    def welcome_message(self):
        print("\n" + "=" * 50)
        print("Welcome to GUESS THE NUMBER!")
        print("=" * 50)
        print("\nRules:")
        print("- Bull: Correct digit at correct position")
        print("- Near-Bull: Correct digit at wrong position")
        print("- Duck: Incorrect digit")
        print("\nGame Modes:")
        print("- Easy: 4-digit number, 4 attempts")
        print("- Medium: 5-digit number, 5 attempts")
        print("- Hard: 6-digit number, 6 attempts")
        print("=" * 50 + "\n")

    def select_mode(self):
        while True:
            print("Select game mode (easy/medium/hard):")
            mode = input("> ").lower()
            if mode in self.modes:
                self.mode = mode
                self.attempts_left = self.modes[mode]["attempts"]
                return
            else:
                print("Invalid mode. Please choose easy, medium, or hard.")

    def generate_secret_number(self):
        digits = self.modes[self.mode]["digits"]
        # Generate a random number with the specified number of digits
        # Ensure no repetitive digits by using a set of available digits
        available_digits = list(range(10))  # 0-9
        random.shuffle(available_digits)
        
        # First digit shouldn't be 0 for proper number length
        if available_digits[0] == 0:
            # Swap with another digit
            swap_index = random.randint(1, 9)
            available_digits[0], available_digits[swap_index] = available_digits[swap_index], available_digits[0]
            
        # Take the first 'digits' number of shuffled digits
        selected_digits = available_digits[:digits]
        self.secret_number = ''.join(map(str, selected_digits))

    def get_guess(self):
        digits = self.modes[self.mode]["digits"]
        while True:
            print(f"\nAttempts left: {self.attempts_left}")
            print(f"Enter a {digits}-digit number:")
            guess = input("> ")
            if guess.isdigit() and len(guess) == digits:
                return guess
            else:
                print(f"Please enter a valid {digits}-digit number.")

    def evaluate_guess(self, guess):
        bulls = 0
        near_bulls = 0
        
        # Count bulls (correct digit at correct position)
        for i in range(len(guess)):
            if i < len(self.secret_number) and guess[i] == self.secret_number[i]:
                bulls += 1
        
        # Count near-bulls (correct digit at wrong position)
        # First, create copies of the digits to handle duplicates properly
        secret_digits = list(self.secret_number)
        guess_digits = list(guess)
        
        # Remove bulls from consideration
        for i in range(len(guess)-1, -1, -1):
            if i < len(secret_digits) and guess[i] == secret_digits[i]:
                secret_digits.pop(i)
                guess_digits.pop(i)
        
        # Count near-bulls
        for digit in guess_digits:
            if digit in secret_digits:
                near_bulls += 1
                secret_digits.remove(digit)
        
        # Calculate ducks
        ducks = len(guess) - bulls - near_bulls
        
        return bulls, near_bulls, ducks

    def display_result(self, bulls, near_bulls, ducks):
        print(f"Bulls: {bulls} | Near-Bulls: {near_bulls} | Ducks: {ducks}")
        
        if bulls == len(self.secret_number):
            print("\n🎉 Congratulations! You guessed the number correctly! 🎉")
            self.game_over = True
        elif self.attempts_left == 0:
            print(f"\nGame over! You've used all your attempts.")
            print(f"The secret number was: {self.secret_number}")
            self.game_over = True

    def play(self):
        self.welcome_message()
        self.select_mode()
        self.generate_secret_number()
        
        while not self.game_over:
            guess = self.get_guess()
            self.attempts_left -= 1
            
            bulls, near_bulls, ducks = self.evaluate_guess(guess)
            self.display_result(bulls, near_bulls, ducks)
            
            if self.attempts_left == 0 and not self.game_over:
                print(f"\nGame over! You've used all your attempts.")
                print(f"The secret number was: {self.secret_number}")
                self.game_over = True
        
        self.play_again()

    def play_again(self):
        print("\nDo you want to play again? (yes/no)")
        choice = input("> ").lower()
        if choice in ["yes", "y"]:
            self.__init__()  # Reset the game
            self.play()
        else:
            print("\nThank you for playing Guess the Number! Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    game = GuessTheNumber()
    game.play()