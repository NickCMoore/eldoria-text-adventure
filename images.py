# Standard library imports
import pyfiglet

# Third party library imports
from colorama import Fore, Style


def main_title():
    title_font = "slant"
    title_text = "Eldoria Text Adventure"
    f = pyfiglet.Figlet(font=title_font, width=80, justify='center')
    game_title = f.renderText(title_text)
    print(Fore.RED + Style.BRIGHT + game_title)
