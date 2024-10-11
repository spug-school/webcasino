import random
from ..Game import Game
from typing import override

class Dice(Game):
    '''
    Game: Dice
    Description: The simplest dice game, where the player determines the number of sides on the dice and then guesses a value of the rolled dice.
    '''
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())
        
        # Game specific attributes
        self.sides = 6

    def _roll_dice(self) -> int:
        return random.randint(1, self.sides)

    def _determine_outcome(self, guess: int, bet: int, roll: int) -> int:
        return bet * self.sides if guess == roll else 0

    @override
    def start_game(self) -> dict:
        '''
        Game-specific logic for: Dice
        '''
        bet = self.get_bet(self.player.get_balance())
            
        # one more opportunity to exit the game before rolling the dice
        if bet == 0:
            return 0
        
        self.sides = self.validate_input('\nKuinka monta sivuista noppaa heitetään (2 - 20): ', 'int', 2, 20)
        guess = self.validate_input(f'\nArvaa nopan arvo (1 - {self.sides}): ', 'int', 1, self.sides)
        roll = self._roll_dice()
        
        return {
            'won': guess == roll,
            'win_amount': self._determine_outcome(guess, bet, roll),
            'bet': bet
        }