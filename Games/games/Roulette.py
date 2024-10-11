import random
from time import sleep
from ..Game import Game
from cli.common.utils import header
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
            'm': 'musta',
            'v': 'vihreä'
        }
        
        # Constant values
        self.color_guesses = 1
        self.number_guesses = 2
        self.roll_history_rolls = 10
        
        self.roll_history = self._create_initial_history()
        
    def _create_initial_history(self) -> list:
        history = []
        
        for i in range(self.roll_history_rolls):
            num = random.randint(0, 36)
            history.append({
                'number': num,
                'color': 'v' if num in self.colors['v'] else 'p' if num in self.colors['p'] else 'm'
            })
            
        return history
    
    def _print_history(self) -> None:
        history_str = "  |  ".join([f'{roll["number"]}-{self.color_names[roll["color"][0]][0].upper()}' for roll in self.roll_history])
        print(f'Viimeiset {self.roll_history_rolls} pyöräytystä:')
        
        self.box_wrapper(history_str)
    
    def _get_color(self, number: int) -> str:
        return 'v' if number in self.colors['v'] else 'p' if number in self.colors['p'] else 'm'
        
    def _get_guesses(self, guess_type: str, guess_count: int, valid_values: tuple) -> list:
        '''
        Get the guesses from the player.
        The guess_type is either 'Väri' or 'Numero'.
        '''
        
        input_type = 'str' if guess_type == 'Väri' else 'int'
        min_value = valid_values[0] if guess_type == 'Numero' else None
        max_value = valid_values[1] if guess_type == 'Numero' else None
        allowed_values = valid_values if guess_type == 'Väri' else None
        
        valid_range = f'{min_value} - {max_value}' if guess_type == 'Numero' else ' / '.join(valid_values)

        return [
            self.validate_input(
                prompt=f'{guess_type}arvaus {i+1}. Syötä tyhjä, jos et arvaa. ({valid_range}): ',
                input_type=input_type,
                min_value=min_value,
                max_value=max_value,
                allowed_values=allowed_values,
                allow_empty=True
            ) for i in range(guess_count)
        ]
        
    def _get_bets(self, guesses: dict) -> list:
        color_bet = [0] if not guesses['color'] else [self.get_bet(self.player.get_balance(), f'Panos väriarvaukselle ({self.color_names[guesses["color"][i]]})') for i in range(self.color_guesses)]
        number_bets = [0, 0] if not guesses['number'] else [self.get_bet(self.player.get_balance(), f'Panos numeroarvaukselle {i+1} ({guesses["number"][i]})') for i in range(self.number_guesses)]
        
        return color_bet + number_bets
                
    def _spin_wheel(self) -> int:
        print('\n\nPyörä pyörii...\n')
        
        sleep(random.randint(1 * 10, 3 * 10) / 10) # sleep for a random time between 0.5 and 1 seconds

        rolled_number = random.randint(0, 36)
        rolled_color = 'v' if rolled_number in self.colors['v'] else 'p' if rolled_number in self.colors['p'] else 'm'

        roll = {
            'number': rolled_number,
            'color': rolled_color,
        }

        # add the new roll to the history
        self.roll_history.insert(0, roll)
    
        # remove the oldest roll
        self.roll_history.pop()
        
        return roll

    def _determine_outcome(self, guesses: list, bets: list, roll: int) -> int:
        total_winnings = 0

        for guess, bet in zip(guesses, bets):
            if isinstance(guess, int) and guess == roll['number']:
                total_winnings += bet * 36

            elif isinstance(guess, str) and guess == roll['color']:
                if guess == 'v':
                    total_winnings += bet * 36
                else:
                    total_winnings += bet * 2

        return total_winnings
    
    @override
    def start_game(self) -> dict:
        '''
        Game-specific logic for: Roulette
        '''
        self._print_history()
        
        # get the guesses before bets
        print('\nArvaukset:')
        color_guesses = self._get_guesses('Väri', self.color_guesses, tuple(self.colors.keys()))
        number_guesses = self._get_guesses('Numero', self.number_guesses, (0, 36))
        guesses = color_guesses + number_guesses
        
        if not any(number_guesses) and not any(color_guesses):
            return None
        
        # get the bets
        print('\nPanostus:')
        bets = self._get_bets({
            'color': color_guesses,
            'number': number_guesses
        })
        total_bet = sum(bets)
        
        # one last chance to leave the game before spinning the wheel
        # -> all bets == 0
        if total_bet == 0:
            return None
        
        roll = self._spin_wheel()
        print(f'\nPyörä pyörähti! Numero: {roll["number"]}, väri: {self.color_names[roll["color"]]}\n')
        
        outcome = self._determine_outcome(guesses, bets, roll)
        
        return {
            'won': outcome > 0,
            'win_amount': outcome,
            'bet': total_bet
        }