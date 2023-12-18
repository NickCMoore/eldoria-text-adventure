# **_Eldoria Text Adventure_**

Eldoria Text Adventure is an interactive and mythical journey where the player takes on the role of an adventurer exploring the enchanting realms of Eldoria. This text-based game combines storytelling, puzzle-solving, and decision-making.

Upon entering their name and selecting a difficulty level, players are transported to a crossroads, initiating the game with an element of player choice. Here, they must decide between three distinct paths: Forest, Town, and Desert, each presenting unique challenges and opportunities.

Opting for the Forest Path involves solving the wise old tree's riddle, while exploring the bustling town introduces encounters with shops, mysterious merchants, and engaging puzzles. Navigating the scorching desert presents decisions impacting the character's health and word puzzles to solve.

Players can track their progress with marked completed paths and a visible health score, aiming to achieve the highest possible score. The game concludes with the final score recorded on the leaderboard, providing a competitive element for players to compare their achievements. 

![Responsive design](assets/images/screen-mockup.png)

### Project purpose

The purpose of the game is to meet the goals of several specific audiences:

**Gaming Enthusiasts:**

Goal - Offer an entertaining and immersive experience in the mythical world of Eldoria, appealing to those who enjoy engaging narratives and decision-based gameplay.

**Strategy Gamers and Puzzle Solvers:**

Goal - Challenge players with strategic decision-making and puzzle-solving elements, encouraging critical thinking and strategic planning.

**Story-Driven Gamers:**

Goal - Provide a dynamic storytelling experience with multiple outcomes, ensuring each playthrough offers a unique and unpredictable adventure.

**Software Developers:**

Goal - Integrate Google Sheets for easy customisation of puzzles, leaderboards and game data, appealing to developers and game designers.

**Puzzle Enthusiasts:**

Goal - Enhance the educational value of the game with puzzles, riddles, and challenges, offering an engaging platform for players to improve their problem-solving skills.

It is built using Python and runs through the Code institute mock terminal on Heroku.


Welcome to <a href="https://eldoria-text-adventure-b67c4e715670.herokuapp.com/" target="_blank" rel="noopener">Eldoria Text Adventure</a>


# Contents

* [**User Experience UX**](<#user-experience-ux>)
    * [User Stories](<#user-stories>)
    * [Game Design](<#gamedesign>)
* [**Current Features**](<#current-features>)
* [**Future Features**](<#future-features>)
* [**Technologies Used**](<#technologies-used>)
* [**Testing**](<#testing>)
* [**Deployment**](<#deployment>)
* [**Credits**](<#credits>)
    * [**Content**](<#content>)
    * [**Media**](<#media>)
*  [**Acknowledgements**](<#acknowledgements>)


# User Experience (UX)

## User Stories

- As a user, I want to easily navigate through the game, understanding where I am and the available options at any given point.
- As a user, I want puzzle-solving elements to be intuitive and enjoyable.
- As a user, I want immediate feedback on my choices and actions in the game.
- As a user, I want to track my progress in the game and see how my choices impact the overall storyline.
- As a user, I want the game's story to be presented in an engaging and immersive way.
- As a user, I want the ability to customise aspects of the game, such as difficulty levels, name or player inventory.
- As a user, I want the game to adapt to different screen sizes and devices.
- As a user, I want visually appealing graphics and designs that enhance the overall gaming experience.

## Game Design

The game's flowchart serves as a visual representation of the player's journey through Eldoria. Starting with the opening screen where players input their name and select a difficulty level, the flowchart branches into three distinct paths – Forest, Town, and Desert. Each path is strategically designed to present unique challenges and encounters, creating a dynamic and varied gameplay experience. There are decisions at critical junctures, representing moments where players must make choices that impact the storyline and their character's health.

## Colour Scheme

As the app was developed for the terminal environment, extensive design elements or colour schemes were not relevant. However, Colorama was utilised strategically to introduce subtle color enhancements to certain aspects of the game. This was done to ensure that crucial information or specific sections of the application would stand out and be easily distinguishable for the user within the terminal interface.

# Current Features

## Game Introduction

Description: Welcomes players to the Eldoria Text Adventure.

User Interaction: Prompts users to enter their name and choose a difficulty level.

Purpose: Sets the stage for the adventure and gathers initial player input.

## Crossroads

Description: Presents players with the crossroads, allowing them to choose different paths.

User Interaction: Players can choose paths, check their backpack, view their score, or quit the game.

Purpose: Serves as a central hub for navigation and decision-making, linking to various game elements.

## Town Path

Description: Simulates the player's encounter in the bustling town of Eldoria.

User Interaction: Offers choices to visit the following areas:
- Potion Shop - Provides a health potion as a gift, impacting the player's health.
- Explore the Market Square - Presents encounters, such as encountering a pickpocket, impacting the player's health
- Talk to the Mysterious Merchant - Presents a puzzle for the player to solve, offering a bonus upon successful completion.

Purpose: Introduces town-specific encounters, decisions, and puzzles.

## Desert Path

Description: Simulates the player's journey through the scorching desert.

User Interaction: Allows the player to choose actions such:
- Search for an oasis - Players make decisions impacting their health and progress.
- Navigate sand dunes - Player has to solve a word puzzle.
- Rest in the shade - Player's health recovers.

Purpose: Presents a unique environment with distinct challenges and decisions.

## Game Over

Description: Displays when the player completes all paths or decides to quit the game.

User Interaction: Prompts the player to decide whether to continue playing or exit the game.

Purpose: Wraps up the game, showcases the final score, and potentially updates the leaderboard.

## Leaderboard

Description: Displays the leaderboard with the top 10 scores.
User Interaction: Allows players to view their final score and compare it with other players.
Purpose: Recognises player achievements and provides a competitive aspect to the game.

# Future Features

## Expand story paths

Introduce new story paths, locations, and characters to further improve the player's adventure.

## Add further character customisation

Allow players to customise their character's appearance, traits, or abilities at the beginning of the game.

## More interactive dialogue

Expand dialogue options and create branching dialogues based on player choices.

## Additional endings

 Develop multiple endings based on the player's choices throughout the game, providing a variety of outcomes and story resolutions.

 # Technologies used

The following technologies were used in the development of the app:

Python: Implemented for content creation and structural elements.
Gitpod: Utilized for app deployment.
GitHub: Served as the code repository for the website.
Heroku: Chosen as the hosting platform for the game.
Diagrams.net: Employed to design the game layout and create a comprehensive flowchart.
Visual Studio Code (VSCode): Used as the primary integrated development environment (IDE) for coding and project management.

# Testing

# Deployment

Code Institute supplied a template for showcasing the terminal view of this backend application in web browser. This enhancement aims to make the project more accessible to a wider audience.

You can access the live deployed application at <a href="https://eldoria-text-adventure-b67c4e715670.herokuapp.com/" target="_blank" rel="noopener">Eldoria Text Adventure</a>

## Local Deployment

VSCode was used to write the code for this project.

To make a local copy of this repository, you can clone the project by typing the follow into your IDE terminal:

git clone https://github.com/nickcmoore/eldoria-text-adventure.git

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

Open in Gitpod

## Heroku Deployment

This project uses Heroku, a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select New in the top-right corner of your Heroku Dashboard, and select Create new app from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select Create App.
- From the new app Settings, click Reveal Config Vars, and set the value of KEY to PORT, and the value to 8000 then select add.
- Further down, to support dependencies, select Add Buildpack.
- The order of the buildpacks is important, select Python first, then Node.js second. (if they are not in this order, you can drag them to rearrange them)
- Heroku needs two additional files in order to deploy properly.
    - requirements.txt
    - Procfile

You can install this project's requirements (where applicable) using: pip3 install -r requirements.txt. If you have your own packages that have been installed, then the requirements file needs updated using: pip3 freeze --local > requirements.txt

The Procfile can be created with the following command: echo web: node index.js > Procfile

For Heroku deployment, follow these steps to connect your GitHub repository to the newly created app:

- In the Terminal/CLI, connect to Heroku using this command: heroku login -i
- Set the remote for Heroku: heroku git:remote -a <app_name> (replace app_name with your app, without the angle-brackets)
- After performing the standard Git add, commit, and push to GitHub, you can now type: git push heroku main

The frontend terminal should now be connected and deployed to Heroku.

# Credits

## Content

## Media

# Acknowledgements

This application was created as part of Portfolio Project 3 for the Full Stack Software Development Diploma at the Code Institute. I express my gratitude to my mentor, Jack Wachira, for his ongoing support provided not only during this project but throughout the entire course. I also extend my thanks to the Slack community and everyone at the Code Institute for their assistance and encouragement.

[Back to top](<#contents>)
