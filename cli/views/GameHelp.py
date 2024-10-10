from enum import Enum
from typing import override
from cli.views.CLIView import CLIView
from cli.common.utils import header, get_prompt, box_wrapper

class GameHelp(CLIView):
    view_name = 'Pelien säännöt'
    
    def __init__(self, db_handler: object, player: object, game_options: Enum):
        super().__init__(db_handler, player, self.view_name)
        
        # View specific attributes
        self.help_options = game_options

    def _get_rules(self, game: str):
        try:
            self.show_header(text = f'{game.capitalize()} - säännöt')
            
            result = self.db.query('SELECT rules FROM game_types WHERE name = %s', (game,))
            box_wrapper(f'{result.get('result')[0][0]}')
            
            input('Paina <Enter> palataksesi takaisin.')
            return 
        except Exception as error:
            print(f'get game help error occurred: {error}')

    @override
    def view(self) -> bool:
        '''
        View-specific logic: GameHelp
        '''
        self.show_header(text = 'Valitse peli')
        
        print('Valitse peli josta haluat lukea säännöt.\n')
        for game in self.help_options:
            if game == self.help_options.TAKAISIN:
                print()
            
            print(f'{game.value}. {game.name.capitalize()}')
            
        option = self.validate_input(f'\n\nValitse peli (1 - {len(self.help_options)}): ', 'int', 1, len(self.help_options))

        if option == len(self.help_options):
            return False
        else:
            self._get_rules(self.help_options(option).name.lower())
            
        return True