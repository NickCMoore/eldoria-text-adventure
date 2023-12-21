import os
import sys
import time
import colorama
from colorama import Fore, Style
from models import Player
from leaderboard import update_leaderboard, show_leaderboard


def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def restart_game(gspread_client):
    """
    Restarts the game by clearing the screen and calling the game_intro function.
    """
    from run import game_intro
    print("Restarting the game...\n")
    clear_screen()
    game_intro(gspread_client)


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
            restart_game(gspread_client)
        elif continue_playing == "no":
            sys.exit()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")