from abc import ABC, abstractmethod
import logging
from datetime import datetime

class Game(ABC):
    '''
    Parent class for all the games. Contains common methods and attributes for the games

    Attributes:
        player (object): The current player object
        db_handler (object): The database handler object
        game_type_name (str): The name of the game type
    '''
    def __init__(self, player: object, db_handler: object, game_type_name: str, ui: str = 'cli'):
        self.player = player
        self.db = db_handler
        self.game_type_record = self._get_game_type_record(value = game_type_name, key = 'name_en')
        self.game_info = {
            'name': self.game_type_record.get('name'),
            'rules': self.game_type_record.get('rules')
        }
        self.ui = ui
        
    @abstractmethod
    def start_game(self):
        pass
    
    def deduct_bet(self, bet: int):
        '''
        Deducts bet from the player's balance & saves the record
        '''
        self.player.update_balance(-bet)
        self.player.save()
    
    def after_game(self, bet: int, win_amount: int):
        '''
        Updates the player values and saves the game to the database
        '''
        try:
            self.update_player_values(
                won = win_amount > 0, 
                win_amount = win_amount, 
                save = True
            )
            
            self.save_game_to_history(
                bet = bet, 
                win_amount = win_amount - bet
            )
        except Exception as error:
            logging.error(f'Error after the game: {error}')
    
    # --------------------------------
    # Database related methods
    # --------------------------------
    def _get_game_type_record(self, value: str, key: str = 'name_en') -> dict | bool:
        '''
        Gets the game type record from the database
        '''
        try:
            query = '''
                SELECT * FROM game_types WHERE {} = %s
            '''.format(key)
            
            result = self.db.query(query, (value,), cursor_settings={'dictionary': True})
            
            if result['result_group']:
                game_type_record = result['result'][0]
                return game_type_record
            else:
                return False
        except Exception as error:
            logging.error(f'Error creating the game type: {error}')
            return False
    
    def update_player_values(self, won: bool, win_amount: int, save: bool = True):
        '''
        Updates all the player values in bulk after a game has ended
        
        Parameters:
            won (bool): Whether the player won the game or not
            win_amount (int): The amount won
            save (bool): Whether to save the updated values to the database
        '''
        try:
            if won: # win
                self.player.update_total_winning(win_amount)
                self.player.update_games_won()
                self.player.update_balance(win_amount) # update balance with net outcome
            else: # loss
                self.player.update_games_lost()
                
                if self.player.get_balance() <= 0:
                    self.player.set_banned()
            
            # win & loss
            self.player.update_games_played()
            
            if self.player.get_balance() <= 0:
                self.player.update_balance(0) # don't allow negative balances

            
            if save: # save the updated values to the database
                self.player.save()
        except Exception as error:
            logging.error(f'Error updating the player values: {error}')
    
    def save_game_to_history(self, win_amount: int, bet: int) -> bool:
        '''
        Saves the game to the database
        '''
        try:
            query = '''
                INSERT INTO game_history
                (bet, win_amount, played_at, user_id, game_type_id)
                VALUES (%s, %s, %s, %s, %s)
            '''
            
            user_id = self.player.get_data().get('id')
            game_type_id = self.db.query('SELECT id FROM game_types WHERE name = %s', (self.game_info.get('name'),), cursor_settings={'dictionary': True})['result'][0].get('id')

            adjusted_win_amount = win_amount if win_amount > 0 else 0
            values = (
                bet, 
                adjusted_win_amount, 
                datetime.now(), 
                int(user_id), 
                int(game_type_id)
            )
            
            result = self.db.query(query, values)
            
            return True if result['affected_rows'] > 0 else False
        except Exception as error:
            logging.error(f'Error saving the game: {error}')
            return False