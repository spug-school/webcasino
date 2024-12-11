import random
from time import sleep
from ..Game import Game
from typing import override

class Roulette(Game):
    '''
    Game: Roulette
    Description: The simplest form of Straight Up roulette bet, where the player guesses the color and/or number of the next roll.
    '''
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())
        
        # Game specific attributes
        self.colors = {
            'v': [0],
            'p': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
            'm': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        }
        self.color_names = {
            'p': 'punainen',
            'm': 'musta'
        }
                
    def _spin_wheel(self) -> int:
        rolled_number = random.randint(0, 36)
        rolled_color = 'v' if rolled_number in self.colors['v'] else 'p' if rolled_number in self.colors['p'] else 'm'

        roll = {
            'number': rolled_number,
            'color': rolled_color,
            'color_name': self.color_names.get(rolled_color)
        }
        
        return roll

    def _determine_outcome(self, guesses: list, bet: list, roll: int) -> int:
        total_winnings = 0
        number_guess_correct = False
        color_guess_correct = False
        
        for guess, bet in zip(guesses, bet):
            if isinstance(guess, int) and guess == roll['number']:
                number_guess_correct = True
                total_winnings += bet * 18

            elif isinstance(guess, str) and guess == roll['color']:
                color_guess_correct = True
                total_winnings += bet * 1.5

        # both guesses are correct, apply a further reduction
        if number_guess_correct and color_guess_correct:
            total_winnings *= 0.75

        return total_winnings
    
    @override
    def start_game(self, bet: int, color_guess: str, number_guess: int) -> dict:
        '''
        Game-specific logic for: Roulette
        '''
        if self.player.get_balance() < bet:
            raise ValueError('Insufficient balance')
    
        self.deduct_bet(bet)

        guesses = (color_guess, number_guess)
        
        roll = self._spin_wheel()
        outcome = self._determine_outcome(guesses, [bet], roll)

        self.after_game(bet, outcome)
        
        return {
            "roll": roll,
            "won": outcome > 0,
            "win_amount": outcome,
            "bet": bet,
            "guesses": guesses,
            'balance': self.player.get_balance()
        }