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

    def _roll_dice(self) -> int:
        return random.randint(1, self.sides)
    
    def _determine_outcome(self, guess: int, bet: int, roll: int, dice_amount: int) -> int:
        return bet * dice_amount * (self.sides/2) if guess == roll else 0

    @override
    def start_game(self, bet: int, dice_amount: int, guess: int) -> dict:
        '''
        Game-specific logic for: Dice
        '''
        if self.player.get_balance() < bet:
            raise ValueError('Insufficient balance')
        
        self.deduct_bet(bet)

        dice_rolls = [self._roll_dice() for _ in range(dice_amount)]
        roll_sum = sum(dice_rolls)
        win_amount = self._determine_outcome(guess, bet, roll_sum, dice_amount)
        game_won = guess == roll_sum
        
        # Bulk-update the player values
        self.update_player_values(
            won = game_won, 
            win_amount = win_amount, 
            save = True
        )
        
        # Save the game to the database
        self.save_game_to_history(
            bet = bet, 
            win_amount = win_amount - bet
        )
        
        return {
            'won': game_won,
            'win_amount': win_amount,
            'bet': bet,
            'dice_rolls': dice_rolls,
            'sum': roll_sum,
            'balance': self.player.get_balance()
        }