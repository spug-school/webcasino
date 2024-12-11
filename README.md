```
__        _______ ____     ____    _    ____ ___ _   _  ___  
\ \      / / ____| __ )   / ___|  / \  / ___|_ _| \ | |/ _ \ 
 \ \ /\ / /|  _| |  _ \  | |     / _ \ \___ \| ||  \| | | | |
  \ V  V / | |___| |_) | | |___ / ___ \ ___) | || |\  | |_| |
   \_/\_/  |_____|____/   \____/_/   \_\____/___|_| \_|\___/ 
```

# CLI Casino

## Table of contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Description

A simple 'casino' application that runs on the web. Allows users to play the most simple casino games with play-money. The app also has some other nice features, such as, a dynamic Leaderboard, the possibility to view the player's own Game history.

### Note
All of the games text are in ***FINNISH*** so do with that as you will.

## Installation

1. Clone the whole repository locally:

   ```sh
   git clone https://github.com/spug-school/webcasino.git
   ```

2. Navigate to the project directory:

   ```sh
   cd path_to_your_instance/webcasino
   ```

3. Install the required Python dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file based off of `.env.example` and add the proper values for your instance.
5. Run the main script with the `--setup` argument to run the database setup:

   ```sh
   python main.py --setup

   // with dummy data
   python main.py --setup --files testdata.sql
   ```
6. Restart the server without the startup flags
7. Navigate to the `web` folder:
    ```sh
    cd web
    ```

    And install npm packages (Vite only)
    ```sh
    npm install
    ```


## Features

- Simple casino games

  - Dice
  - Roulette
  - Twenty One (not working in the web version)
  - Slots
  - Coinflip

- Dynamic Leaderboard
  - Allows the user to choose, what statistic the leaderboard is based on
  - Also allows the user to choose the order (ascending / descending) of the leaderboard
- Auth

  - Asks the user for their username & password before entering the 'casino'

    - Gets the users profile from the database if a record matches the credidentials
    - A new profile is created if the username does not exist

- Player's game history
  - Each played game is saved to the database
  - The user can view their own played games at any time
  - Choose how many games to show
- Profile editing
  - Allows the user to edit their own credentials (username & password)
  - Allows the user to delete their profile and all records from the database
