# Standard library imports
import time
import sympy
import random

# Third party library imports
from colorama import Fore

# Module imports
from run import authorise_gspread, clear_screen
from models import Helmet, Shield

# Constants for worksheet names
WORD_PUZZLE_WORKSHEET = 'word_puzzle'
NUMBER_PUZZLE_WORKSHEET = 'number_puzzle'

# Constants for health-related values
HEALTH_BONUS = 10
HEALTH_PENALTY = 10
MAX_ATTEMPTS_WORD_PUZZLE = 3
MAX_ATTEMPTS_PRIME_PUZZLE = 3
HEALTH_LOSS_MIRAGE = 20

GSPREAD_CLIENT = authorise_gspread()
WORD_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet(WORD_PUZZLE_WORKSHEET)
NUMBER_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet(NUMBER_PUZZLE_WORKSHEET)


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

    max_attempts = MAX_ATTEMPTS_WORD_PUZZLE
    correct_answers = 0

    used_riddles = set()

    while correct_answers < 3:
        current_riddle, answer = random.choice(riddles)

        while current_riddle in used_riddles:
            current_riddle, answer = random.choice(riddles)

        used_riddles.add(current_riddle)

        print(current_riddle)

        player_answer = input("Enter your answer: ").lower()

        if player_answer == answer:
            print("The wise old tree nods in approval.")
            print("Congratulations! You have answered the riddle correctly.")
            player.forest_completed = True
            player.health += HEALTH_BONUS
            correct_answers += 1
            print(
                Fore.GREEN + f"You earned {HEALTH_BONUS} health. Your total score is now {player.health}.")

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
            print(
                Fore.RED + f"Incorrect. You lost {HEALTH_PENALTY} health. The forest path remains a mystery.")
            player.deduct_health(HEALTH_PENALTY)

            max_attempts -= 1
            if max_attempts > 0:
                print(
                    f"You have {max_attempts} {'attempts' if max_attempts > 1 else 'attempt'} left.")
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

    attempts_left = MAX_ATTEMPTS_PRIME_PUZZLE

    while attempts_left > 0:
        player_input = input(
            "Enter your answer as two space-separated prime numbers (e.g., '3 7'): ")

        try:
            num1, num2 = map(int, player_input.split())
            result = check_prime_puzzle(selected_numbers, num1, num2)

            if result:
                print(
                    Fore.GREEN + f"Congratulations, {player.name}! You found the correct pair. You receive a helmet as a bonus!")
                helmet = Helmet()
                player.inventory.add_item(helmet)
                player.mysterious_merchant_completed = True
                break
            else:
                player.deduct_health(HEALTH_PENALTY)
                print("Please try again.")
                attempts_left -= 1

                if attempts_left > 0:
                    print(
                        f"You have {attempts_left} {'attempts' if attempts_left > 1 else 'attempt'} left.")
                else:
                    print(f"{player.name}, you've used all your attempts.")
                    print(
                        Fore.RED + "The correct answer was not found. Better luck next time!")
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


def sand_anagrams(player):
    """
    Recreates the player going on their journey through the sand dunes and solving anagrams on the way.
    """
    from puzzles import word_puzzle, fetch_word_puzzle
    if player.sand_dunes_completed:
        print("You have already navigated the sand dunes.")
        input("Press Enter to continue...")
        return
    clear_screen()
    print("You choose to navigate the arduous sand dunes")
    obstacle_chance = random.randint(1, 10)

    if obstacle_chance <= 8:
        print("You come across a mysterious inscription partially uncovered in the sand...")

        difficulty_word_count = {
            1: 3,
            2: 5,
            3: float('inf')
        }

        word_puzzles = [fetch_word_puzzle() for _ in range(
            difficulty_word_count[player.difficulty])]

        shield_added = False

        for word_puzzle in word_puzzles:
            print(
                f"Unscramble the letters to form a word: {word_puzzle['Scrambled Word']}")

            attempts_left = MAX_ATTEMPTS_WORD_PUZZLE

            while attempts_left > 0:
                player_input = input("Your answer: ").lower()

                if player_input == word_puzzle['Word']:
                    print(Fore.GREEN +
                          "Congratulations! You solved the anagram.")
                    if not shield_added:
                        shield = Shield()
                        player.inventory.add_item(shield)
                        shield_added = True
                    player.sand_dunes_completed = True
                    return
                else:
                    player.deduct_health(HEALTH_PENALTY)
                    print("Please try again.")
                    attempts_left -= 1

                    if attempts_left > 0:
                        print(
                            f"You have {attempts_left} {'attempts' if attempts_left > 1 else 'attempt'} left.")
                    else:
                        print("You've used all your attempts.")
                        print(
                            "The correct answer was not found. Better luck next time!")
                        player.sand_dunes_completed = True
                        return

        print("Congratulations! You successfully navigated the sand dunes.")
        player.sand_dunes_completed = True

    else:
        print(
            Fore.RED + f"You encounter a mirage and end up losing {HEALTH_LOSS_MIRAGE} health.")
        player.deduct_health(HEALTH_LOSS_MIRAGE)

    time.sleep(4)
    input("Press Enter to continue...")
