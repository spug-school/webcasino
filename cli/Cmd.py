import argparse
from enum import Enum

from Games.Dice import Dice
from Games.ventti import Ventti
from Games.Roulette import Roulette
from Games.CoinFlip import CoinFlip
from Games.Slots import Slots
from Player.Player import Player
from cli.GameHelp import GameHelp
from cli.Leaderboard import Leaderboard
from cli.PlayerProfile import PlayerProfile
from cli.utils import clear_terminal, header

class GameOptions(Enum):
    VENTTI = 1
    NOPPAPELI = 2
    RULETTI = 3
    HEDELMAPELI = 4
    KOLIKOHEITTO = 5

class MenuOptions(Enum):
    PELAA = 1
    TULOSTAULUKKO = 2
    ASETUKSET = 3
    OHJEET = 4
    LOPETA = 5

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
            help='Kirjaudu tai rekisteröidy casino cli'
        )
        self.parser.add_argument(
            '--setup',
            action="store_true",
            help="Valmistele Casino cli tietokanta"
        )
        self._run()

    def _run(self):
        args = self.parser.parse_args()

        if args.setup:
            # TODO: ei toimi
            print('Setting up database...')
            self.db.setup_database('./Database/setup.sql')
            return
        elif args.auth:
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
                return 'Väärä argumentti'

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
            header(f'Tervetuloa {self.player.get_username()}', self.player.get_balance())
            self.gameMenu()

    def gameMenu(self):
        for option in MenuOptions:
            print(f'{option.value}. {option.name.capitalize()}')

        try:
            retry = 0
            while retry < 3:
                try:
                    option = int(input('Valitse toiminto: '))
                    break
                except ValueError:
                    print('Virheellinen valinta')
                    retry += 1
        except ValueError:
            print('yritit kolmesti')


        match MenuOptions(option):
            case MenuOptions.PELAA:
                return self.gameSelector()
            case MenuOptions.TULOSTAULUKKO:
                print('Tulostaulukko')
                return Leaderboard(self.db).start_leaderboard()
            case MenuOptions.ASETUKSET:
                print("Asetukset")
                return PlayerProfile(self.db, self.player).start_player_profile()
            case MenuOptions.OHJEET:
                print('Ohjeet')
                return GameHelp(self.db)
            case MenuOptions.LOPETA:
                print('Hyvästi')
                return exit()


    def gameSelector(self):
        print('Saatavilla olevat pelit:')
        for game in GameOptions:
            print(f'{game.value}. {game.name.capitalize()}')

        try:
            game = int(input('Valitse peli: '))

        except ValueError:
            return

        match GameOptions(game):
            case GameOptions.VENTTI:
                return Ventti(self.player, self.db).start_game()
            case GameOptions.DICE:
                return Dice(self.player, self.db).start_game()
            case GameOptions.ROULETTE:
                return Roulette(self.player, self.db).start_game()
            case GameOptions.HEDELMAPELI:
                return Slots(self.player, self.db).start_game()
            case GameOptions.KOLIKOHEITTO:
                return CoinFlip(self.player, self.db).start_game()
