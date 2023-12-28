# Code Validation

Throughout the project, I conducted internal PEP8 validation tests on the Eldoria Text Adventure Game code using the internal PEP8 validation tool installed in VSCode. This enabled me to continuously check to see whether the code was meeting these guidelines.

To install this, I followed the below instructions:

**Install Python Extension:**
Install the "Python" extension in VSCode.
**Install autopep8:**
Run pip install autopep8 in the terminal.
**Configure autopep8 in VSCode:**
Set the path for autopep8 in VSCode settings.
**Enable and Run autopep8:**
Turn on linting in the Status Bar.
Save your file to automatically run autopep8 and highlight PEP8 violations.
**View autopep8 Output:**
Check detailed output in the VSCode Output view.

For further information on this extension, please refer to the following site - <a href="https://eldoria-text-adventure-b67c4e715670.herokuapp.com/" target="_blank" rel="noopener">PEP8</a>

Any issues were usually autocorrected or highlighted in the 'Problem' tab within VSCode.

# Bugs

Aside from regularly documenting smaller bugs through GitHub's commit process, I also used GitHub's issue tracker to monitor and address many of the bugs identified during the development and testing phases of my program. As of now, there are no open bugs, and you can review the historical record of addressed bugs <a href="https://github.com/NickCMoore/eldoria-text-adventure/issues?q=is%3Aissue+is%3Aclosed" target="_blank" rel="noopener">here</a>

![Bugs](assets/images/bugs.png)

# Game Validation Testing

My testing strategy involved validating the core functionalities of the game, ensuring that different paths, encounters, and game mechanics worked as intended. The following areas were tested as a set of test cases:

- Game initialisation and setup
- Player input validation
- Path choices and progression
- Town encounters and events
- Desert path events and puzzles

## Test Cases

1. Game Initialisation

    Scenario 1: Successful Initialisation
    Test Steps:
    - Run the game.
    - Verify that the game initialises without errors.
    Expected Outcome:
    - The game starts without any errors.
    Outcome:
    ![Game Initialisation](assets/images/initialisation.png)
    Result: Pass

2. Player Input

    Scenario 1: Valid Player Name Input
    Test Steps:
    - During player initialisation, enter a valid player name.
    Expected Outcome:
    - The game proceeds without errors.
    Outcome:
    ![Valid Name](assets/images/valid_name.png)
    Result: Pass

    Scenario 2: Invalid Player Name Input
    Test Steps:
    - During player initialisation, enter an invalid player name (e.g., numeric characters).
    Expected Outcome:
    - The game provides an error message and prompts for a valid name.
    Outcome:
    ![Invalid Name](assets/images/invalid_name.png)
    Result: Pass

    Scenario 2: Invalid Difficulty Selection Input
    Test Steps:
    - During player initialisation, player enters invalid difficulty choice (e.g., a, b or c).
    Expected Outcome:
    - The game provides an error message and prompts for a valid number.
    Outcome:
    ![Invalid Difficulty](assets/images/invalid_difficulty.png)
    Result: Pass

3. Crossroads Choices

    Scenario 1: Crossroads
    Test Steps:
    - Choose the Forest Path.
    Expected Outcome:
    - The Forest Path events and puzzles are triggered without errors.
    Outcome:
    ![Forest Path Selection 1](assets/images/forest_path_selection1.png)
    ![Forest Path Selection 2](assets/images/forest_path_selection2.png)
    Result: Pass

    Scenario 2: Town Path
    Test Steps:
    - Choose the Town Path.
    Expected Outcome:
    - Town events and encounters proceed without errors.
    Outcome:
    ![Town Path](assets/images/town_path.png)
    Result: Pass

4. Town Encounters

    Scenario 1: Potion Shop Visit
    Test Steps:
    - Visit the Potion Shop in town.
    Expected Outcome:
    - Player gains health, and the potion shop events complete without errors.
    Outcome:
    ![Potion Shop](assets/images/potion_shop.png)
    Result: Pass

    Scenario 2: Market Square Exploration
    Test Steps:
    Explore the Market Square in town.
    Expected Outcome:
    - Market Square events and encounters proceed without errors.
    Outcome:
    ![Market Square](assets/images/market.png)
    Result: Pass

5. Desert Path

    Scenario 1: Search for Oasis
    Test Steps:
    - Choose to search for an oasis in the desert.
    Expected Outcome:
    - Oasis events and outcomes proceed without errors.
    Outcome:
    ![Oasis](assets/images/oasis.png)
    Result: Pass

    Scenario 2: Navigate Sand Dunes
    Test Steps:
    - Choose to navigate the sand dunes in the desert.
    Expected Outcome:
    - Sand dunes events and puzzles proceed without errors.
    Outcome:
    ![Sand Dunes](assets/images/dunes.png)
    Result: Pass