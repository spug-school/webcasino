import time, random, sys
from typing import override
from ..Game import Game

class Slots(Game):
    '''
    Game: Slots
    Description: A slot machine game where players bet to spin the reels and win based on matching symbols.
    '''
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())

        # Game specific attributes
        self.columns = 4
        self.symbols = ['🍑', '🍌', '🍒', '🍏', '🍇']
        self.win_multipliers = {2: 1.25, 3: 5, 4: 25}

    def _spin_slot_machine(self) -> list:
        final_row = []
        
        for _ in range(self.columns):
            final_row.append(random.choice(self.symbols))

        return final_row

    def _determine_outcome(self, bet: int, final_row: list) -> int:
        winnings = 0
        current_symbol = None
        current_count = 0
        max_consecutive_symbols = 0

        for symbol in final_row:
            if symbol == current_symbol:
                current_count += 1
            else:
                if current_count >= 2:
                    winnings += self.win_multipliers.get(current_count, 0) * bet
                max_consecutive_symbols = max(max_consecutive_symbols, current_count)
                current_symbol = symbol
                current_count = 1

        if current_count >= 2:
            winnings += self.win_multipliers.get(current_count, 0) * bet

        max_consecutive_symbols = max(max_consecutive_symbols, current_count)
        return int(winnings), max_consecutive_symbols

    @override
    def start_game(self, bet: int = None) -> dict:
        '''
        Game-specific logic for: Slots
        '''
        bet = bet or self.bet_amount

        if self.player.get_balance() < bet:
            raise ValueError("Insufficient balance to play the game.")

        self.deduct_bet(bet)

        spin_result = self._spin_slot_machine()
        win_amount, consecutive_symbols = self._determine_outcome(bet, spin_result)

        self.after_game(bet, win_amount)

        return {
            'won': win_amount > 0,
            'win_amount': win_amount - bet,
            'bet': bet,
            'spin_result': spin_result,
            'consecutive_symbols': consecutive_symbols,
            'balance': self.player.get_balance()
        }
