from enum import Enum

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
                    print('Blackjack')
                case HelpOptions.DICE:
                    print('Dice')
                case HelpOptions.ROULETTE:
                    print('Roulette')
                case HelpOptions.SLOTS:
                    print('SLOTS')
                case HelpOptions.Exit:
                    print('Palaa Main menu')
                    break

    def _getHelp(self,game: str):
        try:
            helpData = self._db.query(f'SELECT * FROM help WHERE game = {game}')
            return helpData.get('result')[0]
        except Exception as error:
            print(f'get game help error occurred: {error}')
