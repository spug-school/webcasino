import time, random, sys
from wcwidth import wcswidth
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
        self.bet_amount = 100
        self.spins_per_column = random.randint(3, 8)
        self.columns = 4
        self.symbols = ['🍑', '🍌', '🍒', '🍏', '🍇']
        self.win_multipliers = {2: 1.25, 3: 5, 4: 25}

    def _spin_slot_machine(self) -> list:
        total_spins = self.spins_per_column * self.columns
        final_row = [''] * self.columns

        for spin in range(total_spins):
            row_to_print = []
            for column in range(self.columns):
                if spin >= (column + 1) * self.spins_per_column:
                    row_to_print.append(final_row[column])  # Final symbol
                else:
                    new_symbol = random.choice(self.symbols)
                    row_to_print.append(new_symbol)
                    if spin == (column + 1) * self.spins_per_column - 1:
                        final_row[column] = new_symbol

        return final_row

    def _determine_outcome(self, bet: int, final_row: list) -> int:
        winnings = 0
        current_symbol = None
        current_count = 0

        for symbol in final_row:
            if symbol == current_symbol:
                current_count += 1
            else:
                if current_count >= 2:
                    winnings += self.win_multipliers.get(current_count, 0) * bet
                current_symbol = symbol
                current_count = 1

        if current_count >= 2:
            winnings += self.win_multipliers.get(current_count, 0) * bet

        return int(winnings)

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
        win_amount = self._determine_outcome(bet, spin_result)
        game_won = win_amount > 0

        self.update_player_values(
            won=game_won,
            win_amount=win_amount,
            save=True
        )

        self.save_game_to_history(
            bet=bet,
            win_amount=win_amount - bet
        )

        return {
            'won': game_won,
            'win_amount': win_amount,
            'bet': bet,
            'spin_result': spin_result,
            'balance': self.player.get_balance()
        }
