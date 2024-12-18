import random
from time import sleep
from ..Game import Game
from typing import override

class Coinflip(Game):
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())
        
        # Game specific attributes
        self.coin_sides = [
            ('k', 'kruuna', '👑'),
            ('c', 'klaava', '🍀'),         
        ]
        
    def _flip_coin(self) -> str:
        return random.choice(self.coin_sides)
    
    def _determine_outcome(self, guess: str, flip: str, bet: int) -> int:
        return bet * 2 if guess == flip[0] else 0
    
    @override
    def start_game(self, bet: int, guess: str) -> dict:
        '''
        Game-specific logic for: CoinFlip
        '''
        if self.player.get_balance() < bet:
            raise ValueError('Insufficient balance to play the game.')
        
        self.deduct_bet(bet)

        flip = self._flip_coin()
        win_amount = self._determine_outcome(guess, flip, bet)
        
        self.after_game(bet, win_amount)
        
        return {
            'won': win_amount > 0,
            'win_amount': win_amount,
            'bet': bet,
            'flip': flip,
            'balance': self.player.get_balance()
        }