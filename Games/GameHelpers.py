import logging
from datetime import datetime

class GameHelpers:
    '''
    Helpers: Setup some common game methods that can be used across different games. Should be only used within the game classes.

    Attributes:
        player (dict): The current player object
    '''
    def __init__(self, player: object, game_info: dict, db_handler: object):
        self.player = player # the whole class with the methods included
        self.db = db_handler
        self.game_info = game_info

    # Game related methods
    def get_bet(self) -> int:
        bet = int(input('\nPanos: '))
        
        if bet <= self.player.get_balance():
            self.player.update_balance(-bet)
            return bet
        else:
            print(f'Saldosi on vajaa! Syötä sopiva määrä.\nSaldo: {self.player.get_balance()}')
            return self.get_bet()
        
    def play_again(self) -> bool:
        if self.player.get_balance() <= 0:
            print(f'Saldo ei riitä. Peli päättyi.\n')
            return False
    
        prompt = str(input('Pelataanko uudestaan (k / e): ')).lower()

        match prompt:
            case 'k':
                return True
            case 'e':
                return False
            case _:
                print(f'Virheellinen syöte. Syötä k tai e.')
                return self.play_again()

    # Database related methods
    def update_player_values(self, won: bool, win_amount = int, save = True):
        '''
        Updates all the player values in bulk after a game has ended
        
        @param won: bool: Whether the player won the game or not
        @param win_amount: int: The amount the player won
        @param save: bool: Whether to save the updated values to the database or not
        '''
        if won: # win
            self.player.update_total_winning(win_amount)
            self.player.update_games_won()
        else: # loss
            self.player.update_games_lost()
            
            if self.player.get_balance() <= 0:
                self.player.set_banned()

        self.player.update_games_played()
        self.player.update_balance(win_amount)
        
        if save: # save the updated values to the database
            self.player.save()
    
    def save_game_to_history(self) -> bool:
        '''
        Saves the game to the database. Returns success state boolean
        '''
        # TODO - save the game to the "game_history" table
        try:
            player_id = self.player.get_data().get('id')
            
            # TODO
        except Exception as error:
            logging.error(f'Error saving the game: {error}')
            return False