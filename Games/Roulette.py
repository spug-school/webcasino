import random
from time import sleep
from .GameHelpers import GameHelpers

class Roulette:
    '''
    Game: Roulette
    Description: The simplest form of single guess roulette, where the player chooses a number to bet on and then spins the wheel. Colors are not included in this version, but the number multiplier is faithful, with 0 in the pool too.
    '''
    def __init__(self, player: object, db_handler: object):
        self.player = player
        self.name = 'Ruletti'
        self.rules = 'Pelaaja valitsee numeron sekä mahdollisesti värin, jolle panostaa. Voittokerroin on 36x panos, jos pelaaja arvaa oikean numeron. Oikean värin voittokerroin on 2x panos.'
        self.helpers = GameHelpers(player, {'name': self.name, 'rules': self.rules}, db_handler)

        # the betting options
        # v = green, p = red, m = black
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
        
    def spin_wheel(self) -> int:
        print('\nPyörä pyörii...\n')
        sleep(2)

        rolled_number = random.randint(0, 36)
        rolled_color = 'v' if rolled_number in self.colors['v'] else 'p' if rolled_number in self.colors['p'] else 'm'

        return {
            'number': rolled_number,
            'color': rolled_color,
        }

    def validate_guesses(self, number_guess, color_guess) -> bool:
        '''
        Validates the player's guesses
        '''
        print('\n')

        incorrect_number_msg = 'Virheellinen numeroarvaus. Syötä numero 0 - 36.\n'
        incorrect_color_msg = 'Virheellinen väriarvaus. Syötä "p" tai "m"\n'
        no_guess_msg = 'Sinun täytyy syöttää joko numeroarvaus tai väriarvaus.\n'

        # Check if at least one guess is provided
        if not number_guess and not color_guess:
            print(no_guess_msg)
            return False

        # Validate number guess
        if number_guess:
            if not number_guess.isdigit():
                print(incorrect_number_msg)
                return False
            if not 0 <= int(number_guess) <= 36:
                print(incorrect_number_msg)
                return False

        # Validate color guess
        if color_guess:
            if color_guess.lower() not in ['p', 'm']:
                print(incorrect_color_msg)
                return False

        return True
    
    def determine_outcome(self, number_guess, color_guess, roll: int, bet: int) -> int:
        '''
        Determines the outcome of the game
        '''
        number_correct = number_guess.isdigit() and int(number_guess) == roll['number'] if number_guess else False
        color_correct = color_guess is not None and color_guess == roll['color']

        if number_correct and color_correct:
            return bet * 36 * 2 # both number and color correct
        elif number_correct:
            return bet * 36     # only number correct
        elif color_correct:
            return bet * 2      # only color correct
        else:
            return 0            # neither correct
        
    def start_game(self) -> object:
        '''
        Runs the game and returns the modified player object
        '''
        while True:
            # TODO Header / terminal reload here!!!
            # eg. header('Ruletti', self.player.get_balance())
            self.helpers.game_intro(self.player.get_username())

            bet = self.helpers.get_bet(self.player.get_balance())

            number_guess = input(f'Numeroarvaus\nSyötä tyhjä, jos arvaat vain väriä.\n(0 - 36): ')
            color_guess = input(f'\nVäriarvaus\nSyötä tyhjä, jos arvaat vain numeroa.\n(p/m): ')

            if not self.validate_guesses(number_guess, color_guess):
                self.player.update_balance(bet) # "refund" the bet
                
                # wait for a few seconds before continuing, so the player can read the error messages
                sleep(3)
                continue

            roll = self.spin_wheel()
            
            outcome = self.determine_outcome(number_guess, color_guess, roll, bet)
            net_winnings = outcome - bet
            game_won = outcome > 0

            if game_won:
                # check which guess was correct
                if color_guess == roll['color'] and not number_guess == str(roll['number']):
                    print(f'\nVäriarvaus oli oikein! Voitit {net_winnings} pistettä!\n')
                elif number_guess == str(roll['number']) and not color_guess == roll['color']:
                    print(f'\nNumeroarvaus oli oikein! Voitit {outcome} pistettä!\n')
                else:
                    print(f'\nMolemmat arvauksesi olivat oikein! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nHävisit pelin. Oikea numero oli {roll["number"]} ja väri {self.color_names[roll["color"]]}\n')
            
            # Bulk-update the player values
            self.helpers.update_player_values(game_won, outcome, save = True)
            
            # Save the game to the database
            self.helpers.save_game_to_history(bet = bet, win_amount = outcome)
            
            if not self.helpers.play_again(self.player.get_balance()):
                break

        return self.player