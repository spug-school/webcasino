import random
from ..Game import Game
from typing import override

class Dice(Game):
    '''
    Game: Dice
    Description: A dice game where the player guesses the sum of X amount of rolled dice.
    '''
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())
        
        # Game specific attributes
        self.sides = 6
        self.max_dice = 4

    def _roll_dice(self, dice_amount: int) -> int:
        return sum([random.randint(1, self.sides) for _ in range(dice_amount)])
    
    def _determine_outcome(self, guess: int, bet: int, roll: int, dice_amount: int) -> int:
        return bet * dice_amount if guess == roll else 0

    @override
    def start_game(self, bet: int, dice_amount: int, guess: int) -> dict:
        '''
        Game-specific logic for: Dice
        '''
        self.player.update_balance(-bet)
        self.player.save()
            
        # one more opportunity to exit the game before rolling the dice
        if bet == 0:
            return None
        
        if dice_amount < 2 or dice_amount > self.max_dice:
            raise ValueError(f'Dice amount must be between 2 and {self.max_dice}.')
        
        if guess < dice_amount or guess > self.sides * dice_amount:
            raise ValueError(f'Guess must be between {dice_amount} and {self.sides * dice_amount}.')
        
        
        # dice_amount = self.validate_input(f'\nKuinka montaa noppaa haluat heittää (2 - {self.max_dice}): ', 'int', 2, self.max_dice)
        # dice_total = self.sides * dice_amount
        # guess = self.validate_input(f'\nArvaa noppien summa ({dice_amount} - {dice_total}): ', 'int', dice_amount, dice_total)
        
        roll = self._roll_dice(dice_amount)
        win_amount = self._determine_outcome(guess, bet, roll, dice_amount)
        
        return {
            'won': guess == roll,
            'win_amount': win_amount,
            'bet': bet,
            'roll': roll
        }