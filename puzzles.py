import time
import sympy
import random
import gspread

from colorama import Fore
from run import authorise_gspread
from utils import clear_screen
from models import Helmet, Player

GSPREAD_CLIENT = authorise_gspread()
WORD_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('word_puzzle')
NUMBER_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('number_puzzle')

def word_puzzle(player):
    """
    Simulates the player attempting to solve a series of riddles presented in the enchanted forest.
    """
    print("As you venture deeper into the mystical forest, you encounter a wise old tree.")
    print("The tree speaks in a whisper, presenting you with a riddle:")

    riddles = [
        (Fore.BLUE + "What has keys but can't open locks?", "piano"),
        (Fore.BLUE + "I'm tall when I'm young and short when I'm old. What am I?", "candle"),
        (Fore.BLUE + "I have a heart that doesn't beat. What am I?", "artichoke"),
        (Fore.BLUE + "I fly without wings. I cry without eyes. Wherever I go, darkness follows me. What am I?", "cloud"),
        (Fore.BLUE + "The more you take, the more you leave behind. What am I?", "footsteps")
    ]

    max_attempts = 3
    correct_answers = 0

    while correct_answers < 3:
        current_riddle, answer = random.choice(riddles)
        print(current_riddle)

        player_answer = input("Enter your answer: ").lower()

        if player_answer == answer:
            print("The wise old tree nods in approval.")
            print("Congratulations! You have answered the riddle correctly.")
            player.forest_completed = True
            player.health += 10
            correct_answers += 1
            print(f"You earned 10 points. Your total score is now {player.health}.")

            if correct_answers < 3:
                print("The wise old tree presents you with another riddle.")
            else:
                print("You've successfully answered three riddles!")
                print("You decide to return to the crossroads.")
                time.sleep(3)
                input("Press Enter to return to the crossroads.")
                return
        else:
            print("The wise old tree shakes its branches.")
            print("Incorrect. The forest path remains a mystery.")
            player.deduct_health(10)

            max_attempts -= 1
            if max_attempts > 0:
                print(f"You have {max_attempts} {'attempts' if max_attempts > 1 else 'attempt'} left.")
            else:
                print(f"{player.name}, unfortunate...")
                print("You failed to answer the riddle correctly three times.")
                print("The Forest Path is now disabled (completed).")
                player.forest_completed = True
                time.sleep(3)
                input("Press Enter to return to the crossroads.")
                return



def fetch_word_puzzle():
    """
    Fetches a word puzzle from the 'word_puzzle' worksheet in Google Sheets.
    """
    data = WORD_PUZZLE.get_all_values()
    data_without_header = data[1:]
    random_word_puzzle = random.choice(data_without_header)
    return {'Scrambled Word': random_word_puzzle[0], 'Word': random_word_puzzle[1]}


def mysterious_merchant_puzzle(player):
    """
    Simulates the player talking to the Mysterious Merchant in the town, presenting a puzzle with 8 numbers, including 2 prime numbers.
    """
    if player.mysterious_merchant_completed:
        print("You have already talked to the Mysterious Merchant.")
        return

    clear_screen()
    print(f"{player.name}, you approach the Mysterious Merchant.")
    print("They offer you a puzzle and a chance to gain a bonus.")

    data = NUMBER_PUZZLE.get_all_values()

    all_numbers = [int(num) for num in filter(
        None, [item for sublist in data for item in sublist])]

    if len(all_numbers) < 8:
        print("There are not enough numbers for the puzzle.")
        return

    selected_numbers = random.sample(all_numbers, 8)

    prime_numbers = list(sympy.primerange(2, max(selected_numbers)))

    random_indices = random.sample(range(8), 2)
    for idx in random_indices:
        selected_numbers[idx] = prime_numbers.pop()

    print(f"The Mysterious Merchant presents you with a challenge:")
    print(Fore.BLUE +
          f"Find two prime numbers in the list {selected_numbers}.")

    attempts_left = 3

    while attempts_left > 0:
        player_input = input(
            "Enter your answer as two space-separated prime numbers (e.g., '3 7'): ")

        try:
            num1, num2 = map(int, player_input.split())
            result = check_prime_puzzle(selected_numbers, num1, num2)

            if result:
                print(
                    f"Congratulations, {player.name}! You found the correct pair. You receive a helmet as a bonus!")
                helmet = Helmet()
                player.inventory.add_item(helmet)
                print(f"A {helmet._name} has been added to your backpack.")
                player.mysterious_merchant_completed = True
                break
            else:
                print("Sorry, that's not the correct pair. Try again.")
                attempts_left -= 1

                if attempts_left > 0:
                    print(
                        f"You have {attempts_left} {'attempts' if attempts_left > 1 else 'attempt'} left.")
                else:
                    print(f"{player.name}, you've used all your attempts.")
                    print("The correct answer was not found. Better luck next time!")
                    player.mysterious_merchant_completed = True
                    return
        except ValueError:
            print("Invalid input format. Please enter two space-separated numbers.")
            attempts_left -= 1


def check_prime_puzzle(numbers, num1, num2):
    """
    Checks if the player's input is correct for the prime number puzzle.
    """
    return sympy.isprime(num1) and sympy.isprime(num2) and num1 != num2 and num1 in numbers and num2 in numbers
