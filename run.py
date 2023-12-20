# External libraries
import os
import sys
import time
import random

import gspread
from google.oauth2.service_account import Credentials
import sympy
import colorama
from colorama import Fore, Style
from images import main_title


colorama.init(autoreset=True)

# Google Sheets API integration
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Google credentials
CREDS = Credentials.from_service_account_file('creds.json')


def authorise_gspread():
    """
    Exception raised in event Google Sheets cannot be accessed.
    """
    try:
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
        return GSPREAD_CLIENT
    except Exception as e:
        print(f"Error authorising Google Sheets API: {e}")
        return None


GSPREAD_CLIENT = authorise_gspread()
# Google Sheets worksheets
LEADERBOARD = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('leaderboard')
NUMBER_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('number_puzzle')
WORD_PUZZLE = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('word_puzzle')


# Custom code for items and game logic
class Item:
    def __init__(self, name, description):
        self._name = name
        self._description = description

    def __str__(self):
        return f"{self._name}\n=====\n{self._description}\n"
    

class Sword(Item):
    def __init__(self):
        super().__init__(name="sword", description="A magnificent sword")


class Helmet(Item):
    def __init__(self):
        super().__init__(name="helmet", description="A sturdy helmet for protection")


class Shield(Item):
    def __init__(self):
        super().__init__(name="shield", description="A protective shield")

class Backpack:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)
        print(
            f"Excellent work!\nA {item._name} has been added to your backpack.")

    def display_inventory(self):
        if not self._items:
            print("Your backpack is empty.")
        else:
            print("Items in your backpack:")
            for item in self._items:
                print(item)


class Player:
    """
    Class representing a player.
    """

    def __init__(self, name, difficulty, gspread_client):
        """
        Initialise a player.
        """
        self.name = name
        self.difficulty = difficulty
        self.health = self.set_starting_health()
        self.incorrect_guesses = 0
        self.inventory = Backpack()
        self.initialise_paths()

    def set_starting_health(self):
        """
        Set initial health levels for the player based on difficulty.
        """
        if self.difficulty == 1:
            return 100
        elif self.difficulty == 2:
            return 75
        elif self.difficulty == 3:
            return 50

    def initialise_paths(self):
        self.forest_completed = False
        self.town_completed = False
        self.potion_shop_completed = False
        self.market_square_completed = False
        self.mysterious_merchant_completed = False
        self.oasis_completed = False
        self.shade_completed = False
        self.sand_dunes_completed = False
        self.desert_completed = False

    def deduct_health(self, amount):
        """
        Deduct health from the player if they get it wrong.
        """
        self.health -= amount
        print(f"{self.name}, you lost {amount} health.")
        print(f"Your remaining health is {self.health}.")

    def check_backpack(self):
        """
        Enable the player to check their backpack.
        """
        print("Checking your backpack:")
        self.inventory.display_inventory()
        time.sleep(2)


def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def game_intro(gspread_client):
    """
    Initialises the game, prompts the user for their name and difficulty level, and starts the game.
    """
    print("Welcome to the Eldoria Text Adventure!\n")

    while True:
        player_name = input("Enter your name: \n")

        if player_name and not player_name.isdigit():
            break
        else:
            print("Invalid name. Please enter a valid name without numbers.")

    difficulty = choose_difficulty()
    player = Player(player_name, difficulty, gspread_client)
    print(f"\nYou chose your difficulty level {player.difficulty}.")
    print(f"Your starting health is {player.health}.")
    time.sleep(3)
    clear_screen()
    print(
        f"\nWelcome, {player.name}! You are about to embark on an epic adventure in the mystical realm of Eldoria.")
    print("Your goal is to explore different paths, solve challenges, and earn points.")
    print("Be cautious! Your health is crucial.")
    print("Incorrect choices may lead to deductions...")

    input("Press Enter to begin your journey...\n")
    crossroads(player)

    return player


def choose_difficulty():
    """
    Prompts the user to choose a difficulty level and returns the selected level as an integer.
    """
    print("Choose your difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        choice = input("Which level do you choose (1, 2 or 3) ?\n")
        if choice.isdigit() and choice in ['1', '2', '3']:
            return int(choice)
        else:
            if not choice:
                print("Please enter a value.")
            else:
                print("Invalid choice. Please enter a valid number (1, 2, or 3)")


def crossroads(player):
    """
    Manages the player's choices at the crossroads, allowing them to choose paths, check the backpack, check the score, or quit the game.
    """
    while True:
        clear_screen()
        print("The eternal mists clear...")
        print("You find yourself at a crossroads.")
        print("There are three paths diverging in front of you.")

        if player.forest_completed:
            print("1. The Forest Path (Completed)")
        else:
            print("1. The Forest Path")

        if not player.town_completed:
            print("2. The Town Path")
        else:
            print("2. The Town Path (Completed)")

        if not player.desert_completed:
            print("3. The Desert Path")
        else:
            print("3. The Desert Path (Completed)")

        print("4. Check Backpack")
        print("5. Check Score")
        print("6. Quit")

        while True:
            choice = input("Enter the number relating to your chosen path (1, 2 or 3): ")

            if choice == '1' and player.forest_completed:
                print("The Forest Path is already completed. Choose another option.")
                time.sleep(2)
            elif choice == '2' and player.town_completed:
                print("The Town Path is already completed. Choose another option.")
            elif choice == '3' and player.desert_completed:
                print("The Desert Path is already completed. Choose another option.")
            elif choice == '6':
                if quit_game(player):
                    return
            elif choice == '4':
                player.check_backpack()
            elif choice == '5':
                print(f"Your current score is: {player.health}")
                input("Press Enter to continue...")
            elif choice.isdigit() and choice in ['1', '2', '3']:
                handle_path_choice(player, choice)
            else:
                print(
                    "Invalid choice. Please enter a valid number (1, 2, 3, 4, 5, or 6).")
                continue

            if player.forest_completed and player.town_completed and player.desert_completed:
                print("Congratulations! You have completed all paths.")
                update_leaderboard(player)
                show_leaderboard(player)
                print(f"\n{Fore.RED}GAME OVER!{Style.RESET_ALL}")
                print(f"{player.name}, your final score was {player.health}")
                time.sleep(2)
                sys.exit()

            break


def restart_game(gspread_client):
    """
    Restarts the game by clearing the screen and calling the game_intro function.
    """
    print("Restarting the game...\n")
    clear_screen()
    game_intro(gspread_client)


def update_leaderboard(player):
    """
    Adds the player's score to the leaderboard.
    """
    LEADERBOARD.append_row([player.name, str(player.health)])


def show_leaderboard(player):
    """
    Displays the leaderboard with the top 10 scores.
    """
    clear_screen()
    print("\nLEADERBOARD")
    print("============")

    time.sleep(2)
    data = LEADERBOARD.get_all_values()

    if not data:
        print("No leaderboard data available.")
    else:
        sorted_data = sorted(data[1:], key=lambda x: int(x[1]), reverse=True)

        print(f"{Fore.CYAN}{'Rank':<10}{'Player':<20}{'Score':<10}{Style.RESET_ALL}")
        for rank, row in enumerate(sorted_data[:10], start=1):
            player_name, score = row
            if player_name == player.name:
                print(
                    f"{Fore.GREEN}{rank:<10}{player_name:<20}{score:<10}{Style.RESET_ALL}")
            else:
                print(f"{rank:<10}{player_name:<20}{score:<10}")


def quit_game(player, gspread_client):
    """
    Quits the game and updates the leaderboard if the player has completed at least two paths.
    """
    if not (player.forest_completed and player.town_completed) or \
            (not player.forest_completed and not player.town_completed):
        print("You need to complete at least two paths to appear on the leaderboard.")
    else:
        print("Quitting the game...")
        update_leaderboard(player)
        show_leaderboard(player)
        print(f"\n{Fore.RED}GAME OVER!{Style.RESET_ALL}")
        print(f"{player.name}, your final score was {player.health}")
        time.sleep(2)

    while True:
        continue_playing = input(
            "Do you want to continue playing? (yes/no): ").lower()
        if continue_playing == "yes":
            restart_game()
        elif continue_playing == "no":
            sys.exit()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

# Path functions
def handle_path_choice(player, choice):
    """
    Handles the player's choice of paths (forest, town, desert) and progresses the game accordingly.
    """
    if choice == '1' and not player.forest_completed:
        clear_screen()
        print(f"{player.name}, you venture into the mystical forest.")
        forest_riddle(player)
    elif choice == '2':
        clear_screen()
        print(f"{player.name}, you head into town.")
        town_encounter(player)
    elif choice == '3':
        clear_screen()
        print(f"{player.name}, you enter the scorching desert.")
        desert_path(player)


# Forest Path
def forest_riddle(player):
    """
    Simulates the player attempting to solve the riddle presented in the enchanted forest.
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
    attempts = 0

    for riddle, answer in riddles:
        print(riddle)

        while attempts < max_attempts:
            player_answer = input("Enter your answer: ").lower()

            if player_answer == answer:
                print("The wise old tree nods in approval.")
                print("Congratulations! You have answered the riddle correctly.")
                player.forest_completed = True
                player.health += 10
                print(
                    f"You earned 10 points. Your total score is now {player.health}.")
                return
            else:
                print("The wise old tree shakes its branches.")
                print("Incorrect. The forest path remains a mystery.")
                player.deduct_health(10)

                attempts += 1
                if attempts < max_attempts:
                    print(
                        f"You have {max_attempts - attempts} {'attempts' if max_attempts - attempts > 1 else 'attempt'} left.")
                else:
                    print(f"{player.name}, unfortunate...")
                    print("You failed to answer the riddle correctly three times.")
                    print("The Forest Path is now disabled (completed).")
                    player.forest_completed = True
                    time.sleep(2)
                    input("Press Enter to return to the crossroads.")
                    return

# Town Path functions


def town_encounter(player):
    """
    Simulates an encounter in the town, allowing the player to make choices and progress in the game.
    """
    print("You enter the bustling town of Eldoria.")
    print("People are going about their daily lives, and various shops line the streets.")

    while True:
        time.sleep(4)
        clear_screen()
        print("What will you do in the town?")
        print("1. Visit the Potion Shop")
        print("2. Explore the Market Square")
        print("3. Talk to the Mysterious Merchant")
        print("4. Check Backpack")

        choice = input("Enter the number relating to your choice: ")

        if choice.isdigit() and choice in ['1', '2', '3', '4']:
            if choice == '1':
                visit_potion_shop(player)
                player.potion_shop_completed = True
            elif choice == '2':
                explore_market_square(player)
                player.market_square_completed = True
            elif choice == '3':
                talk_to_mysterious_merchant(player)
                player.mysterious_merchant_completed = True
            elif choice == '4':
                player.check_backpack()
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, or 4).")

        if player.potion_shop_completed and player.market_square_completed and player.mysterious_merchant_completed:
            print("You have visited everywhere in town!")
            input("Press Enter to return to the crossroads...")
            player.town_completed = True
            crossroads(player)
            break


def visit_potion_shop(player):
    """
    Simulates the player visiting the Potion Shop in the town, providing a health potion as a gift.
    """
    if player.potion_shop_completed:
        print("You have already visited the Potion Shop.")
        return

    print("You enter the Potion Shop and meet the friendly shopkeeper.")
    print("They offer you a health potion as a gift.")

    player.health += 20
    print(f"You gained 20 health. Your total health is now {player.health}.")

    player.inventory.add_item(
        Item(name="Health Potion", description="A magical potion that restores health."))

    player.potion_shop_completed = True


def explore_market_square(player):
    """
    Simulates the player exploring the Market Square in the town and encountering a pickpocket.
    """
    if player.market_square_completed:
        print("You have already explored the Market Square.")
        return
    print("You explore the Market Square and find various goods.")
    print("While browsing, you encounter a pickpocket!")

    player.deduct_health(15)

    print("The pickpocket escapes, but you managed to retain most of your belongings.")

    player.market_square_completed = True


def talk_to_mysterious_merchant(player):
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
    
    all_numbers = [int(num) for num in filter(None, [item for sublist in data for item in sublist])]

    if len(all_numbers) < 8:
        print("There are not enough numbers for the puzzle.")
        return

    selected_numbers = random.sample(all_numbers, 8)

    prime_numbers = list(sympy.primerange(2, max(selected_numbers)))

    random_indices = random.sample(range(8), 2)
    for idx in random_indices:
        selected_numbers[idx] = prime_numbers.pop()

    print(f"The Mysterious Merchant presents you with a challenge:")
    print(Fore.BLUE + f"Find two prime numbers in the list {selected_numbers}.")

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

    player.mysterious_merchant_completed = True


def check_prime_puzzle(numbers, num1, num2):
    """
    Checks if the player's input is correct for the prime number puzzle.
    """
    return sympy.isprime(num1) and sympy.isprime(num2) and num1 != num2 and num1 in numbers and num2 in numbers


# Desert Path functions
def desert_path(player):
    """
    Player has to traverse a scorching desert
    """
    while True:
        time.sleep(4)
        clear_screen()
        print("What will you do in the desert?")

        if player.oasis_completed:
            print("1. Search for an oasis (Completed)")
        else:
            print("1. Search for an oasis")

        if player.sand_dunes_completed:
            print("2. Navigate the sand dunes (Completed)")
        else:
            print("2. Navigate the sand dunes")

        if player.shade_completed:
            print("3. Rest in the shade of a rock (Completed)")
        else:
            print("3. Rest in the shade of a rock")

        if player.oasis_completed and player.sand_dunes_completed and player.shade_completed:
            print("Congratulations! You have completed all paths in the desert.")
            print("You decide to return to the crossroads.")
            player.desert_completed = True
            crossroads(player)
            input("Press Enter to continue...")
            time.sleep(4)
            break

        print("4. Check Backpack")
        print("5. Check Score")
        print("6. Quit")

        choice = input("Enter the number relating to your chosen action: ")

        if choice == '1':
            if not player.oasis_completed:
                search_for_oasis(player)
        elif choice == '2':
            if not player.sand_dunes_completed:
                navigate_sand_dunes(player)
        elif choice == '3':
            if not player.shade_completed:
                rest_in_shade(player)
        elif choice == '4':
            player.check_backpack()
        elif choice == '5':
            print(f"Your current score is: {player.health}")
            input("Press Enter to continue...")
        elif choice == '6':
            if quit_game(player):
                break

        if player.sand_dunes_completed and choice == '2':
            print("The Sand Dunes option is no longer available.")
            return

        if player.oasis_completed and choice == '1':
            print("The Search for an Oasis option is now disabled.")
            return

        if player.oasis_completed and player.sand_dunes_completed and player.shade_completed:
            print("You have completed all paths in the desert.")
            print("You decide to return to the crossroads.")
            player.desert_completed = True
            crossroads(player)
            break


def search_for_oasis(player):
    """
    Player searches for an oasis in the desert.
    """
    print("You decide to search for an oasis to quench your thirst.")
    oasis_chance = random.randint(1, 10)

    if oasis_chance <= 7:
        print("You discover a hidden oasis and replenish your water supply.")
        print("You feel refreshed.")
        player.health += 10
        player.oasis_completed = True
        print(
            f"Your health has increased by 10. Your total health is now {player.health}.")
    else:
        print("Unfortunately, you couldn't find an oasis, and the scorching heat takes a toll on you.")
        player.deduct_health(15)
        player.oasis_completed = True


def navigate_sand_dunes(player):
    """
    Recreates the player going on their journey through the sand dunes
    """
    print("You choose to navigate the arduous sand dunes")
    obstacle_chance = random.randint(1, 10)

    if obstacle_chance <= 5:
        print("You come across a mysterious inscription partially uncovered in the sand...")

        difficulty_word_count = {
            1: 3,
            2: 5,
            3: float('inf')
        }

        word_puzzles = [fetch_word_puzzle() for _ in range(
            difficulty_word_count[player.difficulty])]

        for word_puzzle in word_puzzles:
            print(
                f"Unscramble the letters to form a word: {word_puzzle['Scrambled Word']}")

            while True:
                player_input = input("Your answer: ").lower()

                if player_input == word_puzzle['Word']:
                    print("Congratulations! You solved the number puzzle.")
                    add_shield_to_backpack(player)
                    return
                else:
                    print("Incorrect. Try again.")
                    player.deduct_health(15)
                    player.sand_dunes_completed = True
                    if player.sand_dunes_completed:
                        print("You successfully navigated the sand dunes.")
                        break

        print("Congratulations! You successfully navigated the sand dunes.")
    else:
        print("You encounter a mirage and end up wasting time.")

def add_shield_to_backpack(player):
    shield = Shield()
    player.inventory.add_item(shield)
    print(f"A {shield._name} has been added to your backpack.")


def rest_in_shade(player):
    """
    Simulates the player resting in the shade to regain health.
    """
    print("You find a comfortable spot in the shade and rest for a while.")
    print("The cool shade revitalizes you, and you regain 15 health.")

    player.health += 15

    print(f"Your total health is now {player.health}.")

    player.shade_completed = True

    input("Press Enter to continue...")


def fetch_word_puzzle():
    """
    Fetches a word puzzle from the 'word_puzzle' worksheet in Google Sheets.
    """

    data = WORD_PUZZLE.get_all_values()

    data_without_header = data[1:]

    random_word_puzzle = random.choice(data_without_header)

    return {'Scrambled Word': random_word_puzzle[0], 'Word': random_word_puzzle[1]}


def main():
    clear_screen()
    main_title()
    gspread_client = authorise_gspread()
    if gspread_client is None:
        print("Exiting the game due to authorisation error.")
        sys.exit()

    player = game_intro(gspread_client)


if __name__ == "__main__":
    main()
