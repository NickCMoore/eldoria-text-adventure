# Game items

class Item():
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return "{}\n=====\n{}\n".format(self.name, self.description)
    
class Sword(Item):
    def __init__(self):
        super().__init__(name="Sword", description="A magnificent sword pulsating with elemental energy. It resonates with the power of the elements.")

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

game_intro()

