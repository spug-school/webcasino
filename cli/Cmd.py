import argparse
from enum import Enum

from Games.Dice import Dice
from Games.ventti import Ventti
from Player.Player import Player
from cli.GameHelp import GameHelp
from cli.Leaderboard import Leaderboard
from cli.PlayerProfile import PlayerProfile
from cli.utils import clear_terminal, header

class GameOptions(Enum):
    VENTTI = 1
    DICE = 2
    ROULETTE = 3
    SLOTS = 4

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


        # while True:
            # try:
        self.player = Player(username, password, self.db)
     # `           break
            # except Exception as error:
            #     print(f'Virheellinen salasana! Yritä uudelleen.\n')
            #     return error

        print(f'Welcome {username}')
        return self.gameLoop()

    def _register(self) -> str:
        print('Create an account')
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = self.db.query(f"SELECT username FROM users WHERE username = '{username}'")
        if user.get('result') == []:
            self.player = Player(username, password, self.db)
            return f'Username: {username}\nPassword: {password}'
        return 'User already exists'

    def gameLoop(self):
        while True:
            if self.player == 'after playing run this':
                self.player.save()
            clear_terminal()
            header(f'Welcome {self.player.get_username()}', self.player.get_balance())
            self.gameMenu()

    def gameMenu(self):
        for option in MenuOptions:
            print(f'{option.value}. {option.name.capitalize()}')

        option = int(input('Valitse toiminto: '))

        match MenuOptions(option):
            case MenuOptions.PLAY:
                return self.gameSelector()
            case MenuOptions.LEADERBOARD:
                print('Leaderboard')
                return Leaderboard(self.db).start_leaderboard()
            case MenuOptions.SETTINGS:
                print("Asetukset")
                return PlayerProfile(self.db, self.player).start_player_profile()
            case MenuOptions.HELP:
                print('Help')
                return GameHelp(self.db)
            case MenuOptions.EXIT:
                print('Hyvasti')
                return exit()


    def gameSelector(self):
        print('Saatavilla olevat pelit:')
        for game in GameOptions:
            print(f'{game.value}. {game.name.capitalize()}')
        game = int(input('Valitse peli: '))

        match GameOptions(game):
            case GameOptions.VENTTI:
                print('Ventti')
                return Ventti(self.player, self.db).start_game()
            case GameOptions.DICE:
                print('Dice')
                return Dice(self.player, self.db).start_game()
            case GameOptions.ROULETTE:
                print('Roulette')
                return 'Roulette'

