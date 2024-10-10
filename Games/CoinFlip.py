import random
from time import sleep
from .Game import Game
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
        print('\nKolikkoa heitetään...\n')
        sleep(random.randint(1 * 10, 3 * 10) / 10) # sleep for a random time between 0.5 and 1 seconds
        return random.choice(self.coin_sides)
    
    def _determine_outcome(self, guess: str, flip: str, bet: int) -> int:
        return bet * 2 if guess == flip[0] else 0
    
    @override
    def game_specific_logic(self) -> dict:
        '''
        Game-specific logic for: CoinFlip
        '''
        bet = self.get_bet(self.player.get_balance())
        
        # one more opportunity to exit the game before flipping the coin
        if bet == 0:
            return False
        
        guess = self.validate_input('\nArvaa kruuna (k) vai klaava (c): ', 'str', allowed_values = ('k', 'c'))
        flip = self._flip_coin()
        
        return {
            'won': guess == flip[0],
            'win_amount': self._determine_outcome(guess, flip, bet),
            'bet': bet
        }