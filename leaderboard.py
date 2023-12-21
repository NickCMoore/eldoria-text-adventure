import gspread
from google.oauth2.service_account import Credentials
import time


from colorama import Fore, Style

CREDS = Credentials.from_service_account_file('creds.json')

# Google Sheets API integration
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

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


GSPREAD_CLIENT = authorise_gspread()
LEADERBOARD = GSPREAD_CLIENT.open(
    'eldoria-text-adventure').worksheet('leaderboard')



def update_leaderboard(player):
    """
    Adds the player's score to the leaderboard.
    """
    from models import Player
    from run import authorise_gspread
    LEADERBOARD.append_row([player.name, str(player.health)])


def show_leaderboard(player):
    """
    Displays the leaderboard with the top 10 scores.
    """
    from models import Player
    from utils import clear_screen
    clear_screen()
    print("\nLEADERBOARD")
    print("============")

    time.sleep(2)
    data = LEADERBOARD.get_all_values()

    if not data:
        print("No leaderboard data available.")
    else:
        sorted_data = sorted(data[1:], key=lambda x: int(x[1]), reverse=True)

        print(f"{Fore.CYAN}{'Rank':<10}{'Player':<20}{'Score':<10}{Style.RESET_ALL}")
        for rank, row in enumerate(sorted_data[:10], start=1):
            player_name, score = row
            if player_name == player.name:
                print(
                    f"{Fore.GREEN}{rank:<10}{player_name:<20}{score:<10}{Style.RESET_ALL}")
            else:
                print(f"{rank:<10}{player_name:<20}{score:<10}")