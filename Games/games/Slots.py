import time, random, sys
from wcwidth import wcswidth
from typing import override
from ..Game import Game

class Slots(Game):
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())
        
        # Game specific attributes
        self.game_cost = 100
        self.spins_per_column = random.randint(3, 8)
        self.columns = 4
        self.symbols = ['🍑', '🍌', '🍒', '🍏', '🍇'] # add more if needed
        
        # key is the amount of same symbols, value is the multiplier
        self.win_multipliers = {
            2: 1.25,
            3: 5,
            4: 25
        } # if these are changed, make sure to change the database record's "rules" too!
        
    def _clear_row(self, lines: int):
        '''
        Clears the specified number of lines in the terminal to make the game look more authentic
        '''
        sys.stdout.write(f'\033[{lines}F')  # Move cursor up by 'lines' lines
        sys.stdout.flush()
            
    def _print_table(self, row: list):
        col_widths = [wcswidth(symbol) + 3 for symbol in row]

        # generate the table rows
        row_content = "│" + "│".join(f"{symbol:^{width - 1}}" for symbol, width in zip(row, col_widths)) + "│"
        top_row = "┌" + "┬".join("─" * width for width in col_widths) + "┐"
        bottom_row = "└" + "┴".join("─" * width for width in col_widths) + "┘"
        
        print(top_row)
        print(row_content)
        print(bottom_row)
        
    def _spin_slot_machine(self) -> list:
        total_spins = self.spins_per_column * self.columns
        final_row = [''] * self.columns
        
        print("\033[?25l", end='')  # hide the cursor from the machine
        print('\nHedelmäpeli pyörimään!')

        try:
            for spin in range(total_spins):
                # Create the row to print
                row_to_print = []
                for column in range(self.columns):
                    if spin >= (column + 1) * self.spins_per_column:
                        row_to_print.append(final_row[column])  # final symbol for the column
                    else:
                        new_symbol = random.choice(self.symbols)
                        row_to_print.append(new_symbol)
                        if spin == (column + 1) * self.spins_per_column - 1:
                            final_row[column] = new_symbol  # save final symbol
                
                if spin > 0:
                    self._clear_row(3)

                self._print_table(row_to_print)
                
                # add a delay to make the 'machine' look more authentic
                delay_factor = (spin + 1) / total_spins
                time.sleep(0.3 + delay_factor * 0.3)
        finally:
            print("\033[?25h", end='')  # Show the cursor again

        return final_row
        
    def _determine_outcome(self, bet: int, final_row: list) -> int:
        '''
        Determines the outcome and calculates the winnings based on the final row.
        Only gives winnings if the symbols are next to each other.
        '''
        winnings = 0
        current_symbol = None
        current_count = 0
        
        for symbol in final_row:
            if symbol == current_symbol:
                current_count += 1
            else:
                if current_count >= 2:
                    # calc winnings based on the number of consecutive 
                    # symbols and multiply by the bet
                    winnings += self.win_multipliers.get(current_count, 0) * bet
                current_symbol = symbol
                current_count = 1
        
        # check the last sequence
        if current_count >= 2:
            winnings += self.win_multipliers.get(current_count, 0) * bet
        
        return int(winnings)

    @override
    def start_game(self) -> dict:
        '''
        Game-specific logic for: Slots
        '''
        
        bet = self.game_cost
        
        if self.player.get_balance() < bet:
            print('Sinulla ei ole tarpeeksi rahaa pelataksesi tätä peliä. Palataan takaisin...')
            time.sleep(3)
            return None
        
        self.player.update_balance(-bet)
        
        spin_result = self._spin_slot_machine()
        
        outcome = self._determine_outcome(bet, spin_result)
        
        return {
            'won': outcome > 0,
            'win_amount': outcome,
            'bet': bet
        }