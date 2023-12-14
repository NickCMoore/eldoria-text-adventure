import pyfiglet
import colorama
from colorama import Fore, Style

def main_title():
    game_title = pyfiglet.figlet_format("Realms of Eldoria",
                                        font="standard", justify="center", width = 90)
    credits = pyfiglet.figlet_format("By Nick Moore",
                                     font="gothic", justify="center", width = 90)
    print(Fore.RED + Style.BRIGHT + game_title + credits)