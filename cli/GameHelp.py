from enum import Enum

from cli.utils import heading

class HelpOptions(Enum):
    BLACKJACK = 1
    DICE = 2
    ROULETTE = 3
    SLOTS = 4
    Exit = 5

class GameHelp:
    def __init__(self, db):
        self._db = db
        self.run()

    def run(self):
        while True:
            print('Welcome to the Casino Help Section')
            print('Here are the games you can play:')
            for game in HelpOptions:
                print(f'{game.value}. {game.name}')

            option = int(input('Which game do you want to get help? '))

            match HelpOptions(option):
                case HelpOptions.BLACKJACK:
                    print('Ventti')
                    self._getHelp('ventti')
                case HelpOptions.DICE:
                    print(heading('Nopanheitto'))
                    self._getHelp('nopanheitto')
                case HelpOptions.ROULETTE:
                    print('Ruletti')
                    self._getHelp('ruletti')
                case HelpOptions.SLOTS:
                    print('Hedelmäpeli')
                    self._getHelp('hedelmäpeli')
                case HelpOptions.Exit:
                    print('Palaa Main menu')
                    break

    def _getHelp(self,game: str):
        try:
            helpData = self._db.query(f'SELECT rules FROM game_types WHERE name = "{game}"')
            print(f'{helpData.get('result')[0][0]} \n')
            return 
        except Exception as error:
            print(f'get game help error occurred: {error}')
