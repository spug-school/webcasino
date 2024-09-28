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
    def __init__(self, player: dict):
        self.player = player
        self.name = 'Dice'
        self.rules = 'The player has to guess the right value of the dice roll. The player himself determines the number of sides on the dice.'
        self.sides = 6
        self.helpers = GameHelpers(player)

    def rollDice(self):
        '''
        Rolls the dice and returns the result
        '''
        return random.randint(1, self.sides)
    

    def determineOutcome(self, guess: int, roll: int, bet: int):
        '''
        Determines the outcome of the game
        '''
        return bet * self.sides if guess == roll else 0

    def startGame(self) -> dict:
        '''
        Runs the game and returns the player object when done
        '''
        print(f'Welcome to the Dice game, {self.player['username']}!\n')

        while True:
            bet = self.helpers.getBet()
            self.sides = int(input(f'Enter the number of sides on the dice: '))

            if self.sides < 2:
                print('The dice must have at least 2 sides. Please enter a valid number of sides.\n')
                continue

            guess = int(input(f'Enter your guess (1 - {self.sides}): '))
            roll = self.rollDice()
            outcome = self.determineOutcome(guess, roll, bet)

            if outcome > 0:
                print(f'\nCongratulations! You guessed right! You have won {outcome}!\n')
                self.helpers.updatePlayerBalance(outcome, getBalance=True)
            else:
                print(f'\nYou have lost the game. The dice roll was {roll}.\n')

            if not self.helpers.playAgain():
                break

        return self.player
            
# game = Dice({'id': 2, 'username': 'John', 'balance': 125})
# game.startGame()