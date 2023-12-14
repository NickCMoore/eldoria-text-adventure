import pyfiglet
import colorama
from colorama import Fore, Style

def main_title():
    game_title = pyfiglet.figlet_format("Realms of Eldoria",
                                        font="standard", justify="center")
    credits = pyfiglet.figlet_format("By Nick Moore",
                                     font="digital", justify="center")
    print(Fore.CYAN + Style.BRIGHT + game_title)