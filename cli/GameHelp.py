from enum import Enum

from cli.utils import heading

class HelpOptions(Enum):
    VENTTI = 1
    NOPPAPELI = 2
    RULETTI = 3
    HEDELMAPELI = 4
    KOLIKOHEITTO = 5

class GameHelp:
    def __init__(self, db):
        self._db = db
        self.run()

    def run(self):
        while True:
            print(heading('Tervetuloa pelien ohjeet osion!'))
            print('Tässä on pelit joista on ohjeet.')
            print('Voit valita pelin ohjeen valitsemalla sen numeroa.\n')
            for game in HelpOptions:
                print(f'{game.value}. {game.name}')

            try:
                option = int(input('\nMistä pelistä haluassa apua? <palaa napsauttaessa ENTER>: '))
            except ValueError:
                return

            match HelpOptions(option):
                case HelpOptions.VENTTI:
                    print('Ventti')
                    self._getHelp('ventti')
                case HelpOptions.NOPPAPELI:
                    print(heading('Nopanheitto'))
                    self._getHelp('nopanheitto')
                case HelpOptions.RULETTI:
                    print('Ruletti')
                    self._getHelp('ruletti')
                case HelpOptions.HEDELMAPELI:
                    print('Hedelmäpeli')
                    self._getHelp('hedelmäpeli')
                case HelpOptions.KOLIKOHEITTO:
                    print('Kolikoheitto')
                    self._getHelp('kolikoheitto')


    def _getHelp(self,game: str):
        try:
            helpData = self._db.query(f'SELECT rules FROM game_types WHERE name = "{game}"')
            print(f'{helpData.get('result')[0][0]} \n')
            return 
        except Exception as error:
            print(f'get game help error occurred: {error}')
