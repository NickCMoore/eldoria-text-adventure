"""
Imported dependencies
"""

import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Style
from images import main_title

import os
import time
import sys
import random


colorama.init(autoreset=True)


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('eldoria-text-adventure')

LEADERBOARD = GSPREAD_CLIENT.open('eldoria-text-adventure').worksheet('leaderboard')
NUMBER_PUZZLE = GSPREAD_CLIENT.open('eldoria-text-adventure').worksheet('number_puzzle')

# Game items

class Item:
    def __init__(self, name, description):
        """
        Initialize an item.
        """
        self.name = name
        self.description = description

    def __str__(self):
        """
        String of the item.
        """
        return "{}\n=====\n{}\n".format(self.name, self.description)


class Sword(Item):
    """
    Class representing a generic item.
    """
    def __init__(self):
        """
        Initialize sword item.
        """
        super().__init__(name="sword", description="A magnificent sword")


class Backpack:
    """
    Class representing a backpack.
    """
    def __init__(self):
        """
        Initialize backpack.
        """
        self.items = []

    def add_item(self, item):
        """
        Add an item to the backpack.
        """
        self.items.append(item)
        print(f"Excellent work!")
        print(f"A {item.name} has been added to your backpack.")

    def display_inventory(self):
        """
        Display the items in the backpack.
        """
        if not self.items:
            print("Your backpack is empty.")
        else:
            print("Items in your backpack:")
            for item in self.items:
                print(item.name)


class Player:
    """
    Class representing a player.
    """
    def __init__(self, name, difficulty):
        """
        Initialize a player.
        """
        self.name = name
        self.difficulty = difficulty
        self.health = self.set_starting_health()
        self.incorrect_guesses = 0
        self.inventory = Backpack()
        self.forest_completed = False
        self.town_completed = False
        self.potion_shop_completed = False
        self.market_square_completed = False
        self.mysterious_merchant_completed = False
        self.oasis_completed = False
        self.shade_completed = False 
        self.sand_dunes_completed = False

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
        if not self.inventory.items:
            print("Your backpack is empty.")
        else:
            self.inventory.display_inventory()

        time.sleep(2)

def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_difficulty():
    """
    Prompts the user to choose a difficulty level and returns the selected level as an integer.
    """
    print("Choose your difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        choice = input("Which level do you choose?\n")
        if choice.isdigit() and choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice. Please enter a valid number (1, 2, or 3)")

def restart_game():
    """
    Restarts the game by clearing the screen and calling the game_intro function.
    """
    print("Restarting the game...\n")
    clear_screen()
    game_intro()

def show_leaderboard(player):
    """
    Displays the leaderboard with the top 10 scores.
    """
    clear_screen()
    print("\nLEADERBOARD")
    print("============")

    time.sleep(2)
    data = SHEET.worksheet('leaderboard').get_all_values()

    if not data:
        print("No leaderboard data available.")
    else:
        sorted_data = sorted(data[1:], key=lambda x: int(x[1]), reverse=True)

        print(f"{Fore.CYAN}{'Rank':<10}{'Player':<20}{'Score':<10}{Style.RESET_ALL}")
        for rank, row in enumerate(sorted_data[:10], start=1):
            player_name, score = row
            if player_name == player.name: 
                print(f"{Fore.GREEN}{rank:<10}{player_name:<20}{score:<10}{Style.RESET_ALL}")
            else:
                print(f"{rank:<10}{player_name:<20}{score:<10}")

def update_leaderboard(player):
    """
    Adds the player's score to the leaderboard.
    """
    LEADERBOARD.append_row([player.name, str(player.health)])

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

        choice = input("Enter the number relating to your chosen path: ")

        if choice == '1' and player.forest_completed:
            print("The Forest Path is already completed. Choose another option.")
            time.sleep(2)
            continue
        elif choice == '2' and player.town_completed:
            print("The Town Path is already completed. Choose another option.")
            time.sleep(2)
            continue
        elif choice == '3' and player.desert_completed:
            print("The Desert Path is already completed. Choose another option.")
            time.sleep(2)
            continue
        elif choice == '6':
            if quit_game(player):
                break 

        if choice == '4':
            player.check_backpack()
        elif choice == '5':
            print(f"Your current score is: {player.health}")
            input("Press Enter to continue...")
        elif choice.isdigit() and choice in ['1', '2', '3']:
            handle_path_choice(player, choice)
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, 4, 5, or 6).")

        if player.forest_completed and choice == '1':
            print("The Forest Path is no longer available.")
            continue

def quit_game(player):
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

    continue_playing = input("Do you want to continue playing? (yes/no): ").lower()
    if continue_playing == "yes":
        crossroads(player)
    else:
        sys.exit()

def town_encounter(player):
    """
    Simulates an encounter in the town, allowing the player to make choices and progress in the game.
    """
    print("You enter the bustling town of Eldoria.")
    print("People are going about their daily lives, and various shops line the streets.")
    print("As you explore, you come across a mysterious merchant offering you a choice.")

    while True:
        print("What will you do in the town?")
        print("1. Visit the Potion Shop")
        print("2. Explore the Market Square")
        print("3. Talk to the Mysterious Merchant")
        print("4. Check Backpack")

        choice = input("Enter the number relating to your choice: ")

        if choice.isdigit() and choice in ['1', '2', '3', '4']:
            handle_town_choice(player, choice)
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, or 4).")

def handle_town_choice(player, choice):
    """
    Handles the player's choices in the town, updating the game state accordingly.
    """
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

    if player.potion_shop_completed and player.market_square_completed and player.mysterious_merchant_completed:
        print("You have visited everywhere in town!")
        input("Press Enter to return to the crossroads...")
        player.town_completed = True
        crossroads(player)

def visit_potion_shop(player):
    """
    Simulates the player visiting the Potion Shop in the town, providing a health potion as a gift.
    """
    if player.potion_shop_completed:
        print("You have already visited the Potion Shop.")
        return
    
    print("You enter the Potion Shop and meet the friendly shopkeeper.")
    print("They offer you a health potion as a gift.")

    # Increase player's health
    player.health += 20
    print(f"You gained 20 health. Your total health is now {player.health}.")

    # Add health potion to player's inventory
    player.inventory.add_item(Item(name="Health Potion", description="A magical potion that restores health."))

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

    # Deduct health for the encounter
    player.deduct_health(15)

    print("The pickpocket escapes, but you managed to retain most of your belongings.")

    player.market_square_completed = True

def talk_to_mysterious_merchant(player):
    """
    Simulates the player talking to the Mysterious Merchant in the town, presenting a puzzle and offering a bonus for solving it.
    """
    if player.mysterious_merchant_completed:
        print("You have already talked to the Mysterious Merchant.")
        return

    print(f"{player.name}, you approach the Mysterious Merchant.")
    print("They offer you a puzzle and a chance to gain a bonus.")

    # Get four random numbers from the number_puzzle worksheet
    data = NUMBER_PUZZLE.get_all_values()
    nums = [int(num) for num in random.choice(data)]

    target = random.randint(1, 1000)

    print("The Mysterious Merchant presents you with a challenge:")
    print(f"Find two numbers in the list {nums} that add up to {target}.")

    attempts_left = 3

    while attempts_left > 0:
        player_input = input("Enter your answer as two space-separated numbers (e.g., '3 7'): ")

        result = check_number_puzzle(nums, target, player_input)

        if result:
            print(f"Congratulations, {player.name}! You found the correct pair. You receive a bonus!")
            break
        else:
            print("Sorry, that's not the correct pair. Try again.")
            attempts_left -= 1

            if attempts_left > 0:
                print(f"You have {attempts_left} {'attempts' if attempts_left > 1 else 'attempt'} left.")

    if attempts_left == 0:
        print(f"{player.name}, you've used all your attempts.")
        print("The correct answer was not found. Better luck next time!")

    player.mysterious_merchant_completed = True

def check_number_puzzle(nums, target, player_input):
    """
    Checks if the player's input is correct for the number puzzle.
    """
    try:
        num1, num2 = map(int, player_input.split())
    except ValueError:
        return False 

    if num1 + num2 == target and num1 in nums and num2 in nums:
        return True  
    else:
        return False  

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

def desert_path(player):
    """
    Player has to traverse a scorching desert
    """
    print(f"{player.name}, you enter the scorching desert.")
    print("The sun beats down mercilessly as you traverse the vast expanse of sand.")

    while True:
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

        print("4. Check Backpack")
        print("5. Check Score")
        print("6. Quit")

        choice = input("Enter the number relating to your chosen action: ")

        if choice == '6':
            if quit_game(player):
                break

        if choice == '4':
            player.check_backpack()
        elif choice == '5':
            print(f"Your current score is: {player.health}")
            input("Press Enter to continue...")
        elif choice.isdigit() and choice in ['1', '2', '3']:
            handle_desert_choice(player, choice)
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, 4, 5, or 6).")

def handle_desert_choice(player, choice):
    """
    Handles the player's choices in the desert, updating the game state accordingly.
    """
    if choice == '1':
        search_for_oasis(player)
    elif choice == '2':
        navigate_sand_dunes(player)
    elif choice == '3':
        rest_in_shade(player)
    elif choice == '4':
        player.check_backpack()
    elif choice == '5':
        print(f"Your current score is: {player.health}")
        input("Press Enter to continue...")
    elif choice == '6':
        if quit_game(player):
            return
            
    if player.oasis_completed and player.sand_dunes_completed and player.shade_completed:
        print("You have completed all of your travels in the desert.")
        print("You decide to return to the crossroads.")
        input("Press Enter to continue to the crossroads...")
        crossroads(player)

    input("Press Enter to continue to the crossroads...")
    crossroads(player)

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
        print(f"Your health has increased by 10. Your total health is now {player.health}.")
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
        print("You encounter a mirage and end up wasting time.")
    else:
        print("You come across a mysterious inscription partially uncovered in the sand...")

        difficulty_word_count = {
            1: 3,
            2: 5,
            3: float('inf')
        }

        failed_attempts = 0

        word_puzzles = [fetch_word_puzzle() for _ in range(difficulty_word_count[player.difficulty])]

        for word_puzzle in word_puzzles:
            print(f"Unscramble the letters to form a word: {word_puzzle['Scrambled Word']}")
            player_input = input("Your answer: ").lower()

            if player_input == word_puzzle['Word']:
                print("Congratulations! You solved the word puzzle and gained +10 health")
                player.health += 10
            else:
                print("Sorry, that's not the right answer. The stone inscription falls on your foot and you lose -10 health")
                player.deduct_health(15)
                failed_attempts += 1

            if failed_attempts >= 3:
                print("You failed the word puzzle three times. Unlucky.")
                player.sand_dunes_completed = True
                input("Press Enter to continue...")
                return

        print("Congratulations! You successfully navigated the sand dunes.")

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
    word_puzzle_worksheet = GSPREAD_CLIENT.open('eldoria-text-adventure').worksheet('word_puzzle')

    data = word_puzzle_worksheet.get_all_values()

    data_without_header = data[1:]

    random_word_puzzle = random.choice(data_without_header)

    return {'Scrambled Word': random_word_puzzle[0], 'Word': random_word_puzzle[1]}


def game_intro():
    """
    Initializes the game, prompts the user for their name and difficulty level, and starts the game.
    """
    print("Welcome to the Eldoria Text Adventure!\n")

    while True:
        player_name = input("Enter your name: \n")
        if player_name and not player_name.isdigit():
            break
        else:
            raise ValueError("Invalid name. No numbers or blanks allowed")
    difficulty = choose_difficulty()
    player = Player(player_name, difficulty)
    print(f"{player_name}, you chose difficulty level {player.difficulty}.")
    print(f"Your starting health is {player.health}")
    crossroads(player)

    return player

def forest_riddle(player):
    """
    Simulates the player encountering a riddle in the enchanted forest and handles the player's attempts to solve it.
    """
    print("As you enter the enchanted forest, you encounter a wise old tree.")
    print("The tree speaks with a mystical voice:")
    print("I speak without a mouth and hear without ears.")
    print("I have no body, but I come alive with the wind. What am I?")

    solve_riddle(player)

def solve_riddle(player):
    """
    Simulates the player attempting to solve the riddle presented in the enchanted forest.
    """
    correct_answer = "an echo"

    for _ in range(3):
        player_answer = input("Enter your answer: ").lower()

        if player_answer == correct_answer:
            print("The wise old tree nods.")
            print("You have answered the riddle correctly.")
            print("You receive a pulsating sword with elemental energy.")
            print("It resonates with the power of the elements.")
            print("You decide to return to the crossroads")
            player.inventory.add_item(Sword()) 
            player.forest_completed = True  

            time.sleep(4)

            return
        
        print("Incorrect. The wise old tree offers a clue:")
        print("I am a sound that repeats. What am I?")

        player.deduct_health(10) 
        player.incorrect_guesses += 1
    
    print(f"{player.name}, unfortunate...")
    print("You failed to answer the riddle correctly three times.")

    if not player.forest_completed:
        print("The Forest Path is now disabled (completed).")

        time.sleep(4)

        input("Press Enter to return to the crossroads...")
        player.forest_completed = True

def main():
    clear_screen()
    main_title()
    player = game_intro()

if __name__ == "__main__":
    main()

