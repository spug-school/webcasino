import argparse
from enum import Enum

from Games.Dice import Dice
from Games.ventti import Ventti
from Player import Player
from cli.Leaderboard import Leaderboard
from cli.utils import clear_terminal, header

class Games(Enum):
    BLACKJACK = 1
    DICE = 2
    SLOTS = 3

class MenuOptions(Enum):
    PLAY = 1
    LEADERBOARD = 2
    SETTINGS = 3
    HELP = 4
    EXIT = 5

class Cmd:
    def __init__(self, db):
        self.db = db
        self.player = None
        self.parser = argparse.ArgumentParser(description="CLI CASINO")
        self.parser.add_argument(
            '--version',
            action='version',
            version='CLI Casino 1.0'
        )
        self.parser.add_argument(
            '--auth',
            help='Sign in or sign up to the casino'
        )
        self._run()

    def _run(self):
        args = self.parser.parse_args()

        if args.auth:
            return self.auth()
        else:
            return self.parser.print_help()

    def auth(self):
        match self.parser.parse_args().auth.split(' ')[0]:
            case 'signup':
                return self._register()
            case 'signin':
                return self._signin()
            case _:
                return 'Invalid argument'

    # TODO: refactor to use the Player class
    def _signin(self):
        auth = self.parser.parse_args().auth
        if len(auth.split(' ')) == 3:
            username = auth.split(' ')[1]
            password = auth.split(' ')[2]
        else:
            username = input('Enter username: ')
            password = input('Enter password: ')
        db = self.db
        user = db.query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")

        if user.get('result') == []:
            return 'Invalid credentials'

        self.player = Player(username, self.db)

        print(f'Welcome {username}')
        return self.gameLoop()

    # TODO: refactor to use the Player class
    def _register(self) -> str:
        print('Create an account')
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = self.db.query(f"SELECT username FROM users WHERE username = '{username}'")
        if user.get('result') == []:
            self.db.query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            self.db.query(f"INSERT INTO user_statistics (user_id) VALUES ((SELECT id FROM users WHERE username = '{username}'))")
            return f'Username: {username}\nPassword: {password}'
        return 'User already exists'

    def gameLoop(self):
        while True:
            if self.player == 'after playing run this':
                self.player.save()
            clear_terminal()
            header('Main menu', self.player.get_balance())
            self.gameMenu()

    def gameMenu(self):
        for option in MenuOptions:
            print(f'{option.value}. {option.name.capitalize()}')

        option = int(input('Select an option: '))

        match MenuOptions(option):
            case MenuOptions.PLAY:
                return self.gameSelector()
            case MenuOptions.LEADERBOARD:
                print('Leaderboard')
                return Leaderboard(self.db).start_leaderboard()
            case MenuOptions.HELP:
                print('Help')
                return 'Help'
            case MenuOptions.EXIT:
                print('Goodbye')
                return exit()


    def gameSelector(self):
        print('Available games:')
        for game in Games:
            print(f'{game.value}. {game.name.capitalize()}')
        game = int(input('Select a game: '))

        match Games(game):
            case Games.BLACKJACK:
                print('Blackjack')
                return Ventti().run()
            case Games.DICE:
                print('Dice')
                return Dice(self.player, self.db).start_game()
            case Games.SLOTS:
                print('Slots')
                return 'Slots'

