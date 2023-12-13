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

# Introduction
def game_intro():
    print("Welcome to the Eldoria Text Adventure!\n")
    player_name = input("Enter your name: ")
    difficulty = choose_difficulty()
    player = Player(player_name, difficulty)

game_intro()
