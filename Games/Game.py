from abc import ABC, abstractmethod
import logging
from datetime import datetime
from cli.common.utils import header, get_prompt, box_wrapper as box_wrap

class Game(ABC):
    '''
    Parent class for all the games. Contains the common methods and attributes for the games

    Attributes:
        player (object): The current player object
        db_handler (object): The database handler object
        game_type_name (str): The name of the game type
    '''
    def __init__(self, player: object, db_handler: object, game_type_name: str, ui: str = 'cli'):
        self.player = player
        self.db = db_handler
        self.game_type_record = self.__get_game_type_record(value = game_type_name, key = 'name_en')
        self.game_info = {
            'name': self.game_type_record.get('name'),
            'rules': self.game_type_record.get('rules')
        }
        self.ui = ui
        
    @abstractmethod
    def start_game(self) -> dict:
        '''
        This method should be implemented in the game class to handle the game-specific logic
        
        Returns:
            dict{}: A dictionary containing the following keys:
                - bet (int): The amount bet.
                - win_amount (int): The amount won.
                - won (bool): Whether the bet was won.
        '''
        pass
    
    def deduct_bet(self, bet: int) -> int:
        '''
        Gets the bet from the player and deducts it from the player's balance
        
        Parameters:
            bet (int): The bet amount
        Returns:
            int: The bet amount
        '''
        self.player.update_balance(-bet)
        self.player.save()
        return bet
    
    # --------------------------------
    # Main game loop
    # --------------------------------
    def run_game(self) -> object:
        '''
        Play the game and return the modified player object
        
        Returns:
            object: The modified player object
        '''
        while True:
            self.game_intro(self.player.get_username())
            
            # check if the player wants to play the game or not
            if not self.play_game():
                break
            
            header(self.game_info.get('name').capitalize(), self.player.get_balance())
            
            # game-specific logic happens here
            outcome = self.start_game()
            
            # cancel if the outcome is not valid (False or None)
            # this can be for example if the player cancels the game via
            # empty bet etc.
            if not outcome:
                continue
            
            game_won = outcome.get('won')
            bet = outcome.get('bet')
            win_amount = outcome.get('win_amount')
            
            if outcome.get('won'):
                print(f'\nOnnittelut! Voitit {outcome.get("win_amount")} pistettä!\n')
            else:
                print(f'\nHävisit pelin.\n')
            
            # Bulk-update the player values
            self.update_player_values(
                won = game_won, 
                win_amount = win_amount, 
                save = True
            )
            
            # Save the game to the database
            self.save_game_to_history(
                bet = bet, 
                win_amount = win_amount - bet
            )
            
            # ask the player if they want to play again, 
            # and break the loop if they don't
            if not self.play_again(self.player.get_balance()):
                break
            
    
    # --------------------------------
    # Database related methods
    # --------------------------------
    def __get_game_type_record(self, value: str, key: str = 'name_en') -> dict | bool:
        '''
        Creates a new game type in the database. References the class name as the game type name
        
        Parameters:
            value (str): The value to search for in the database
            key (str): The key to search for in the database
            
        Returns:
            (dict{} | bool(False)): The game type record, if found. False if not found
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
            
        Returns:
            bool: Success state
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
                
            return True
        except Exception as error:
            logging.error(f'Error updating the player values: {error}')
            return False
    
    def save_game_to_history(self, win_amount: int, bet: int) -> bool:
        '''
        Saves the game to the database. Returns success state boolean
        
        Parameters:
            win_amount (int): The amount won
            bet (int): The amount bet
        
        Returns:
            bool: Success state
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
            values = (bet, adjusted_win_amount, datetime.now(), int(user_id), int(game_type_id))
            
            result = self.db.query(query, values)
            
            if result['affected_rows'] > 0:
                return True
            else:
                raise Exception('Unexpected error saving the game')
        except Exception as error:
            logging.error(f'Error saving the game: {error}')
            return False