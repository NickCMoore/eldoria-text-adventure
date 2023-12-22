# Standard library imports
import time

# Third party library imports
from colorama import Fore

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
        print(Fore.RED + f"{self.name}, you lost {amount} health.")
        print(f"Your remaining health is {self.health}.")

    def check_backpack(self):
        """
        Enable the player to check their backpack.
        """
        print("Checking your backpack...")
        self.inventory.display_inventory()
        time.sleep(2)

    def add_shield_to_backpack(self):
        shield = Shield()
        self.inventory.add_item(shield)
        print(Fore.GREEN + f"A {shield._name} has been added to your backpack.")


# Player class and custom code
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
        print(Fore.GREEN +
            f"A {item._name} has been added to your backpack.")

    def display_inventory(self):
        if not self._items:
            print("Your backpack is empty.")
        else:
            print("Items in your backpack:")
            for item in self._items:
                print(item)