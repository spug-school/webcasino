class GameHelpers:
    '''
    Helpers: Setup some common game methods that can be used across different games. Should be only used within the game classes.

    Attributes:
        player (dict): The current player object
    '''
    def __init__(self, player: dict):
        self.player = player

    def getBet(self) -> int:
        bet = int(input('Enter your bet: '))
        
        if bet <= self.player['balance']:
            self.updatePlayerBalance(bet * -1)
            return bet
        else:
            print(f'Insufficient balance! Please enter a valid bet.\nCurrent balance: {self.player['balance']}')
            return self.getBet()

    def updatePlayerBalance(self, amount: int, getBalance: bool = False) -> int:
        self.player['balance'] += amount
        if getBalance:
            print(f'Current balance: {self.getCurrentBalance()}')
        return self.player['balance']
    
    def getCurrentBalance(self) -> int:
        return self.player['balance']

    def playAgain(self) -> bool:
        print('\n')
        
        if self.player['balance'] <= 0:
            print(f'Out of balance! Cant play anymore.')
            return False
    
        prompt = input('Play again? (y/n): ').lower()

        match prompt:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print(f'Invalid input. Please enter either "y" or "n".')
                return self.playAgain()