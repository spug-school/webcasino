import random
from .GameHelpers import GameHelpers

class Dice:
    '''
    Game: Dice
    Description: The simplest dice game, where the player determines the number of sides on the dice and then guesses a value of the rolled dice.

    Examples:
        dice_game = Dice({'id': 2, 'username': 'John', 'balance': 125})\n
        dice_game.startGame()
    Attributes:
        player (str): The name of the player
        rules (str): The rules of the game
        sides (int): The number of sides on the dice
        max_dice (int): The maximum number of dice that can be rolled
        dice_sum (int): The sum of the dice rolls
    '''
    def __init__(self, player: object):
        self.player = player
        self.name = 'Dice'
        self.rules = 'Pelaaja valitsee itse, kuinka suurta noppaa heittää. Pelaajan tulee sitten arvata nopan oikea silmäluku.'
        self.sides = 6
        self.helpers = GameHelpers(player)

    def rollDice(self) -> int:
        '''
        Rolls the dice and returns the result
        '''
        return random.randint(1, self.sides)

    def determineOutcome(self, guess: int, roll: int, bet: int) -> int:
        '''
        Determines the outcome of the game
        '''
        return bet * self.sides if guess == roll else 0

    def startGame(self) -> dict:
        '''
        Runs the game and returns the player object when done
        '''
        print(f'Tervetuloa nopanheittoon, {self.player.get_username()}!\n')
        print(f'Pelin säännöt: {self.rules}\n')
        
        while True:
            bet = self.helpers.getBet()
            self.sides = int(input(f'Montako sivua nopassa on: '))

            if self.sides < 2:
                print('Nopassa on oltava yli 2 sivua. Syötä muu luku.\n')
                continue

            guess = int(input(f'Syötä arvauksesi (1 - {self.sides}): '))
            roll = self.rollDice()
            
            outcome = self.determineOutcome(guess, roll, bet)
            game_won = outcome > 0

            if outcome > 0:
                print(f'\nOnnittelut! Arvasit oikein! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nHävisit pelin. Oikea arvo oli {roll}.\n')
                
            # Bulk-update the player values
            self.helpers.updatePlayerValues(game_won, outcome, save = True)
            
            if not self.helpers.playAgain():
                break

        return self.player # return the updated player object