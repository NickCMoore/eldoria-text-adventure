# Game items

class Item():
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return "{}\n=====\n{}\n".format(self.name, self.description)
class Sword(Item):
    def __init__(self):
        super().__init__(name="sword", description="A magnificent sword pulsating with elemental energy. It resonates with the power of the elements.")

class Backpack:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Excellent work! A {item.name} has been added to your backpack.")

    def display_inventory(self):
        if not self.items:
            print("Your backpack is empty.")
        else:
            print("Items in your backpack:")
            for item in self.items:
                print(item.name)

# Characters

class Characters:
    def __init__(self, name, description):
        self.name = name

class Wizard(Characters):
    def __init__(self, name, description):
        super().__init__(name="Wizard", description="Eldron the Wise is a venerable wizard with a long white beard and a staff adorned with mystical runes.")

class Player:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.health = self.set_starting_health()
        self.incorrect_guesses = 0
        self.inventory = Backpack()

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
        print(f"{self.name}, you lost {amount} health. Your remaining health is {self.health}.")

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
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice. Please enter a valid number")

def restart_game():
    """
    Function to restart the game
    """
    print("Restarting the game...\n")
    game_intro()

def crossroads(player):
    """
    Function for introducing player path choice at the start of the game
    """
    print("The eternal mists clear. You find yourself at a crossroads with three paths diverging in front of you.")
    print(f"Which will you take {player.name}?")

    while True:
        print("1. The Forest Path")
        print("2. The Town Path")
        print("3. The Desert Path")

        choice = input("Enter the number relating to your chosen path: ")

        if choice in ['1', '2', '3']:
            handle_path_choice(player, choice)
            break
        else:
            print("Invalid choice. Please enter a valid number.")

def handle_path_choice(player, choice):
    if choice == '1':
        print(f"{player.name}, you venture into the mystical forest.")
        forest_riddle(player)    
    elif choice == '2':
        print(f"{player.name}, you head into town.")
    elif choice == '3':
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
            raise ValueError("Invalid name. Please enter a name without numbers or that is blank")
            
    difficulty = choose_difficulty()
    player = Player(player_name, difficulty)
    print(f"{player_name}, you chose difficulty level {player.difficulty}. Your starting health is {player.health}")
    
    crossroads(player)

def forest_riddle(player):
    print("As you enter the enchanted forest, you encounter a wise old tree.")
    print("The tree speaks with a mystical voice:")
    print("I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?")

    solve_riddle(player)

def solve_riddle(player):
    correct_answer = "an echo"

    for _ in range(3): # Three player attempts allowed
        player_answer = input("Enter your answer: ").lower()

        if player_answer == correct_answer:
            print("The wise old tree nods. You have answered the riddle correctly.")
            player.inventory.add_item(Sword()) # Adds the sword to the player's inventory
            break
        else:
            print("Incorrect. The wise old tree offers a clue:")
            print("I am a sound that repeats. What am I?")

            player.deduct_health(10) # Deducts 10 health from the player if they get it wrong
            player.incorrect_guesses += 1

            if player.incorrect_guesses == 3:
                print(f"{player.name}, you've failed to answer the riddle correctly three times. You have died.")
                restart_game()


            retry = input("Do you want to try again? (yes/no): ").lower()
            if retry != "yes":
                print(f"{player.name}, you decide to leave the forest for now.")
                break

if __name__== "__main__":
    game_intro()

