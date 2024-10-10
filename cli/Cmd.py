import argparse
from enum import Enum
from time import sleep

# player class
from Player.Player import Player

# database class
from Database.Database import Database

# cli parts
from cli.views.CLIView import CLIView # base class for views
from cli.views import * # import all views

# menu enums
from cli.common.MenuOptions import MenuOptions, ViewClasses
from cli.common.GameOptions import GameOptions, GameClasses, create_game_options

# games
from Games import * # import all games
 
# common utils
from cli.common.utils import header, fetch_game_types, get_prompt

class Cmd:
    def __init__(self, config: dict):
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
            nargs='*',
            help="Valmistele Casino cli tietokanta. Esim --setup, --setup test.sql"
        )
        self._run(config = config)

    def _run(self, config: dict):
        args = self.parser.parse_args()
        
        # create a db instance
        self.db = Database(
            config = config,
            connect = True,
            setup = {
                'sql': args.setup,
                'source': args.setup if args.setup else []
            }
        )
        
        # create the game selection options
        self._create_games()

        # check if the auth argument is present
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
                return 'Väärä argumentti'

    def _signin(self):
        auth = self.parser.parse_args().auth
        if len(auth.split(' ')) == 3:
            username = auth.split(' ')[1]
            password = auth.split(' ')[2]
        else:
            username = get_prompt('Enter username: ', 'str', allow_empty = False, sanitize = True)
            password = get_prompt('Enter password: ', 'str', allow_empty = False, sanitize = True)

        self.player = Player(username, password, self.db)
        return self.game_loop()

    def _register(self) -> str:
        username = get_prompt('Enter username: ', 'str', allow_empty = False, sanitize = True)
        password = get_prompt('Enter password: ', 'str', allow_empty = False, sanitize = True)
        
        check_exists = self.db.query('SELECT username FROM users WHERE username = %s', (username,))
        
        if not check_exists['result_group']: # user does not exist -> create it
            self.player = Player(username, password, self.db)
            return True
        
        return 'User already exists'
    
    def _create_games(self):
        '''
        Creates the game menu enum based on the available games in the db
        '''
        global GameOptions, GameClasses
        game_types = fetch_game_types(self.db)
        GameOptions, GameClasses = create_game_options(game_types)
    
    def game_loop(self):
        while True:
            header(f'Tervetuloa, {self.player.get_username()}', self.player.get_balance())
            self.main_menu()

    def main_menu(self):
        for option in MenuOptions:
            if option == MenuOptions.LOPETA:
                print()
                
            fixed_option_name = option.name.replace('_', ' ').capitalize()
            print(f'{option.value}. {fixed_option_name}')
            
        option = get_prompt(f'\n\nValitse toiminto (1 - {len(MenuOptions)}): ', 'int', 1, len(MenuOptions), allow_empty = False)
        selected_option = MenuOptions(option)
        
        if selected_option == MenuOptions.PELIVALIKKO:
            header('Valitse peli', self.player.get_balance())
            
            if self.player.get_ban_status() == 1:
                print('Sinulla on aktiivinen porttikielto, et pääse pelaamaan.\n')
                sleep(3)
                return self.game_loop()
            
            return self.game_selection()
        elif selected_option == MenuOptions.LOPETA:
            print(f'\nTervetuloa uudelleen, {self.player.get_username()}!\n')
            self.player.save() # save the player's data once more before exiting
            return exit()
        elif selected_option.name in ViewClasses:
            view_class = ViewClasses[selected_option.name]
            if view_class:
                if selected_option == MenuOptions.PELIEN_SÄÄNNÖT:
                    return view_class(self.db, self.player, GameOptions).run()
                else:
                    return view_class(self.db, self.player).run()
        else:
            print(f'Virheellinen valinta! Valitse numerolla 1 - {len(MenuOptions)}')
            
    def game_selection(self):
        for option in GameOptions:
            if option == GameOptions.TAKAISIN:
                print()
                
            print(f'{option.value}. {option.name.capitalize()}')
            
        option = get_prompt(f'\n\nValitse peli (1 - {len(GameOptions)}): ', 'int', 1, len(GameOptions), allow_empty = False)

        if option in GameOptions:
            game_option_name = GameOptions(option).name
            game_class_name = GameClasses[game_option_name].value
            
            game_class = globals()[game_class_name]
            
            # start the game
            return game_class(self.player, self.db).run_game()
        elif option == GameOptions.TAKAISIN or option == len(GameOptions):
            return self.game_loop()
        else:
            print(f'Virheellinen valinta! Valitse numerolla 1 - {len(GameOptions)}')