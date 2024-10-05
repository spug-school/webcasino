import argparse
from enum import Enum

class Games(Enum):
    BLACKJACK = 1
    DICE = 2
    SLOTS = 3

class MenuOptions(Enum):
    PLAY = 1
    LEADERBOARD = 2
    HELP = 3
    EXIT = 4

class Cmd:
    def __init__(self, db) -> None:
        self.db = db
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

    def run(self) -> str | None:
        args = self.parser.parse_args()

        if args.auth:
            return self.auth()
        else:
            return self.parser.print_help()

    def auth(self) -> str:
        match self.parser.parse_args().auth.split(' ')[0]:
            case 'signup':
                return self._register()
            case 'signin':
                return self._signin()
            case _:
                return 'Invalid argument'

    def _signin(self) -> str:
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

        print(f'Welcome {username}')
        return self.gameMenu()

    def _register(self) -> str:
        print('Create an account')
        username = input('Enter username: ')
        password = input('Enter password: ')
        db = self.db
        user = db.query(f"SELECT username FROM users WHERE username = '{username}'")
        if user.get('result')[0][0] == username:
            return 'User already exists'
        db.query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        return f'Username: {username}\nPassword: {password}'

    def gameMenu(self):
        for option in MenuOptions:
            print(f'{option.value}. {option.name.capitalize()}')

        option = int(input('Select an option: '))
        print(MenuOptions(option))
        print(MenuOptions.PLAY)
        match MenuOptions(option):
            case MenuOptions.PLAY:
                return self.gameSelector()
            case MenuOptions.LEADERBOARD:
                print('Leaderboard')
                return 'Leaderboard'
            case MenuOptions.HELP:
                print('Help')
                return 'Help'
            case MenuOptions.EXIT:
                print('Goodbye')
                return exit()


    def gameSelector(self) -> str:
        GAMES = ('blackjack', 'dice', 'slots')

        print('Available games:')
        for i, game in enumerate(GAMES):
            print(f'{i+1}. {game.capitalize()}')
        game = input('Select a game: ')
        return GAMES[int(game)-1]


