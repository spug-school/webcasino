from enum import Enum

from cli.utils import header, get_prompt, box_wrapper

class GameHelp:
    def __init__(self, db, game_options: Enum):
        self._db = db
        self.help_options = game_options
        self.run()

    def run(self):
        while True:
            header('Pelien säännöt', hide_balance=True)
            
            print('Valitse peli josta haluat lukea säännöt.\n')
            for game in self.help_options:
                if game == self.help_options.TAKAISIN:
                    print()
                
                print(f'{game.value}. {game.name.capitalize()}')

            option = get_prompt(f'\n\nValitse peli (1 - {len(self.help_options)}): ', 1, len(self.help_options), is_numeric=True)

            if option == len(self.help_options):
                return
            else:
                print(self.help_options(option).name.capitalize())
                self._getHelp(self.help_options(option).name.lower())

    def _getHelp(self, game: str):
        try:
            header(f'{game.capitalize()} - säännöt', hide_balance=True)
            
            game = game.lower()
            helpData = self._db.query('SELECT rules FROM game_types WHERE name = %s', (game,))
            box_wrapper(f'{helpData.get('result')[0][0]}')
            
            input('Paina <Enter> palataksesi takaisin.')
            return 
        except Exception as error:
            print(f'get game help error occurred: {error}')
