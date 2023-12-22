import time
import os
import sys
import random
import sympy

from colorama import Fore, Style
from models import Player, Item, Shield
from leaderboard import update_leaderboard, show_leaderboard
from utils import clear_screen, quit_game


# Initial Path Choices

def crossroads(player):
    """
    Manages the player's choices at the crossroads, allowing them to choose paths, check the backpack, check the score, or quit the game.
    """
    clear_screen()
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
            choice = input(
                "Enter the number relating to your chosen path (1, 2 or 3): ")
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


def handle_path_choice(player, choice):
    """
    Handles the player's choice of paths (forest, town, desert) and progresses the game accordingly.
    """
    from puzzles import word_puzzle
    if choice == '1' and not player.forest_completed:
        clear_screen()
        print(f"{player.name}, you venture into the mystical forest...")
        word_puzzle(player)
    elif choice == '2':
        clear_screen()
        print(f"{player.name}, you head into town...")
        town_encounter(player)
    elif choice == '3':
        clear_screen()
        print(f"{player.name}, you enter the scorching desert...")
        desert_path(player)


# Town Path

def town_encounter(player):
    """
    Simulates an encounter in the town, allowing the player to make choices and progress in the game.
    """
    from puzzles import mysterious_merchant_puzzle
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
                mysterious_merchant_puzzle(player)
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
    clear_screen()
    print("You enter the Potion Shop and meet the friendly shopkeeper.")
    print("They offer you a health potion as a gift.")

    player.health += 20
    print(Fore.GREEN + f"You gained 20 health. Your total health is now {player.health}.")

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
    clear_screen()
    print("You explore the Market Square and find various goods.")
    print("While browsing, you encounter a pickpocket!")

    player.deduct_health(15)

    print(Fore.RED + "The pickpocket escapes, you lose 15 health, but manage to retain most of your belongings.")

    player.market_square_completed = True


# Desert Path
    
def desert_path(player):
    from puzzles import sand_anagrams
    oasis_completed = player.oasis_completed
    sand_dunes_completed = player.sand_dunes_completed
    shade_completed = player.shade_completed

    def quit_option():
        if quit_game(player):
            return True
        else:
            return False

    while True:
        time.sleep(4)
        clear_screen()
        print("What will you do in the desert?")
        print("1. Search for an oasis")
        print("2. Navigate the sand dunes")
        print("3. Rest in the shade of a rock")
        print("4. Check Backpack")

        choice = input("Enter the number relating to your choice: ")

        if choice.isdigit() and choice in ['1', '2', '3', '4']:
            if choice == '1':
                search_for_oasis(player)
                player.oasis_completed = True
            elif choice == '2':
                sand_anagrams(player)
                player.sand_dunes_completed = True
            elif choice == '3':
                rest_in_shade(player)
                player.shade_completed = True
            elif choice == '4':
                player.check_backpack()
        else:
            print("Invalid choice. Please enter a valid number (1, 2, 3, or 4).")

        if player.oasis_completed and player.sand_dunes_completed and player.shade_completed:
            print("You have visited everywhere in the desert!")
            input("Press Enter to return to the crossroads...")
            player.desert_completed = True
            crossroads(player)
            break


def search_for_oasis(player):
    """
    Player searches for an oasis in the desert.
    """
    if player.oasis_completed:
        print("You have already searched for an oasis.")
        return

    print("You decide to search for an oasis to quench your thirst.")
    oasis_chance = random.randint(1, 10)

    if oasis_chance <= 5:
        print("You discover a hidden oasis and replenish your water supply.")
        print("You feel refreshed.")
        player.health += 10
        player.oasis_completed = True
        print(
            f"Your health has increased by 10. Your total health is now {player.health}.")
    else:
        print(Fore.RED + "Unfortunately, you couldn't find an oasis, and the scorching heat takes a toll on you.")
        player.deduct_health(15)
        player.oasis_completed = True

    time.sleep(4)
    input("Press Enter to continue...")


def rest_in_shade(player):
    """
    Simulates the player resting in the shade to regain health.
    """
    if player.shade_completed:
        print("You have already rested in the shade.")
        input("Press Enter to continue...")
        return

    print("You find a comfortable spot in the shade and rest for a while.")
    print(Fore.GREEN + "The cool shade revitalizes you, and you regain 15 health.")

    player.health += 15
    player.shade_completed = True

    print(f"Your total health is now {player.health}.")
    input("Press Enter to continue...")
