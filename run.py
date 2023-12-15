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


colorama.init(autoreset=True)  # Colours auto-reset after being printed


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('eldoria-text-adventure')

leaderboard = GSPREAD_CLIENT.open('eldoria-text-adventure').worksheet('leaderboard')

# Game items

class Item():
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return "{}\n=====\n{}\n".format(self.name, self.description)


class Sword(Item):
    def __init__(self):
        super().__init__(name="sword", description="A magnificent sword")


class Backpack:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Excellent work!")
        print(f"A {item.name} has been added to your backpack.")

    def display_inventory(self):
        if not self.items:
            print("Your backpack is empty.")
        else:
            print("Items in your backpack:")
            for item in self.items:
                print(item.name)


class Player:
    def __init__(self, name, difficulty):
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

    def set_starting_health(self):
        """
        Set initial health levels for the player
        """
        if self.difficulty == 1:
            return 100
        elif self.difficulty == 2:
            return 75
        elif self.difficulty == 3:
            return 50

    def deduct_health(self, amount):
        """
        Deducts health from the player if they get it wrong
        """
        self.health -= amount
        print(f"{self.name}, you lost {amount} health.")
        print(f"Your remaining health is {self.health}.")

    def check_backpack(self):
        """
        Enable the player to check their backpack
        """
        print("Checking your backpack:")
        if not self.inventory.items:
            print("Your backpack is empty.")
        else:
            self.inventory.display_inventory()

        time.sleep(2)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_difficulty():
    """
    Function for selecting difficulty level
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
    Function to restart the game
    """
    print("Restarting the game...\n")
    clear_screen()
    game_intro()


def show_leaderboard(player):
    clear_screen()
    print("\nLEADERBOARD")
    print("============")

    time.sleep(2)
    # Fetch updated data from leaderboard worksheet
    data = SHEET.worksheet('leaderboard').get_all_values()

    if not data:
        print("No leaderboard data available.")
    else:
        # Display the leaderboard in a table
        print(f"{Fore.CYAN}{'Rank':<10}{'Player':<20}{'Score':<10}{Style.RESET_ALL}")
        for rank, row in enumerate(data[1:11], start=1):
            player_name, score = row
            if player_name == player.name:  # Highlight player's entry
                print(f"{Fore.GREEN}{rank:<10}{player_name:<20}{score:<10}{Style.RESET_ALL}")
            else:
                print(f"{rank:<10}{player_name:<20}{score:<10}")

def update_leaderboard(player):
    # Add the player's score to the leaderboard
    leaderboard.append_row([player.name, str(player.health)])

def crossroads(player):
    while True:
        clear_screen() 
        print("The eternal mists clear_screen.")
        print("You find yourself at a crossroads.")
        print("There are three paths diverging in front of you.")

        # Display forest path status
        if player.forest_completed:
            print("1. The Forest Path (Completed)")
        else:
            print("1. The Forest Path")

        if not player.town_completed:
            print("2. The Town Path")
        else:
            print("2. The Town Path (Completed)")
    
        print("3. The Desert Path")
        print("4. Check Backpack")
        print("5. Check Score")  

        choice = input("Enter the number relating to your chosen path: ")

        if choice == '1' and player.forest_completed:
            print("The Forest Path is already completed. Choose another option.")
            time.sleep(2)
            continue
        elif choice == '2' and player.town_completed:
            print("The Town Path is already completed. Choose another option.")
            time.sleep(2)
            continue

        if choice == '4':
            player.check_backpack()
        elif choice == '5':
            print(f"Your current score is: {player.health}")
            input("Press Enter to continue...")
        elif choice.isdigit() and choice in ['1', '2', '3']:
            handle_path_choice(player, choice)
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, 4, or 5).")

        if player.forest_completed and choice == '1':
            print("The Forest Path is no longer available.")
            continue


def town_encounter(player):
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
    if player.mysterious_merchant_completed:
        print("You have already talked to the Mysterious Merchant.")
        return
    print(f"{player.name}, you approach the Mysterious Merchant.")
    print("They offer you a puzzle and a chance to gain a bonus.")

    nums = [2, 7, 11, 15]
    target = 9
    
    print("The Mysterious Merchant presents you with a challenge:")
    print(f"Find two numbers in the list {nums} that add up to {target}.")

    # Player attempts the puzzle
    result = find_two_numbers(nums, target)

    # Evaluate player's response
    if result:
        print(f"Congratulations, {player.name}! You found the indices {result}. You receive a bonus!")
    else:
        print("Sorry, that's not the correct pair. Better luck next time!")

    player.mysterious_merchant_completed = True


def find_two_numbers(nums, target):
    """
    Function to find two numbers in a list that add up to the target.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None

        
def handle_path_choice(player, choice):
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


# Introduction
def game_intro():
    """
    Function for initial player parameters
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
    print("As you enter the enchanted forest, you encounter a wise old tree.")
    print("The tree speaks with a mystical voice:")
    print("I speak without a mouth and hear without ears.")
    print("I have no body, but I come alive with the wind. What am I?")

    solve_riddle(player)


def solve_riddle(player):
    correct_answer = "an echo"

    for _ in range(3):  # Three player attempts allowed
        player_answer = input("Enter your answer: ").lower()

        if player_answer == correct_answer:
            print("The wise old tree nods.")
            print("You have answered the riddle correctly.")
            print("You receive a pulsating sword with elemental energy.")
            print("It resonates with the power of the elements.")
            player.inventory.add_item(Sword())  # Adds sword to player backpack
            player.forest_completed = True  # Records completion of forest path
            return
        
        print("Incorrect. The wise old tree offers a clue:")
        print("I am a sound that repeats. What am I?")

        player.deduct_health(10)  # Deducts 10 health if incorrect
        player.incorrect_guesses += 1
    
    print(f"{player.name}, unfortunate...")
    print("You failed to answer the riddle correctly three times.")

    if not player.forest_completed:
        print("The Forest Path is now disabled (completed).")
        input("Press Enter to return to the crossroads...")
        player.forest_completed = True


def game_over(player):
    print(f"\n{Fore.RED}GAME OVER!{Style.RESET_ALL}")
    print(f"{player.name}, your final score was {player.health}")
    time.sleep(2)

        # Update the leaderboard with the player's score
    update_leaderboard(player)
    
    # Show the leaderboard at the end of the game
    show_leaderboard(player)

    
    # Allow the player to restart the game
    restart = input("Do you want to play again? (yes/no): ").lower()
    if restart == "yes":
        restart_game()
    else:
        print("Thanks for playing - see you again soon!")
        sys.exit()

def main():
    clear_screen()
    main_title()
    player = game_intro()
    game_over(player)


if __name__ == "__main__":
    main()
