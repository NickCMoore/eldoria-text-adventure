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
from models import Player
from locations import crossroads
from utils import clear_screen, restart_game

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


colorama.init(autoreset=True)

# Google Sheets API integration
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Google credentials
CREDS = Credentials.from_service_account_file('creds.json')

# Google Sheets worksheets
GSPREAD_CLIENT = authorise_gspread()


def main():
    clear_screen()
    main_title()
    if GSPREAD_CLIENT is None:
        print("Exiting the game due to authorisation error.")
        sys.exit()

    player = game_intro(GSPREAD_CLIENT)


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


if __name__ == "__main__":
    main()
    restart_game()

    while True:
        crossroads()
