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
        
        # Create the game type in the database
        self.create_game_type()

    # Game related methods
    def get_bet(self, balance: int) -> int:
        bet = input(f'Panos (saldo: {balance}): ')

        if not bet.isdigit() or int(bet) <= 0:
            print('Virheellinen syöte. Syötä numero.')
            return self.get_bet(balance)
        
        bet = int(bet)
        
        if bet <= balance:
            self.player.update_balance(-bet)
            return bet
        else:
            print(f'Saldosi on vajaa! Syötä sopiva määrä.\nSaldo: {self.player.get_balance()}')
            return self.get_bet(balance)
        
    def play_again(self, balance: str) -> bool:
        if balance <= 0:
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
                return self.play_again(balance)
    
    def game_intro(self, username: str):
        print(f'Tervetuloa {self.game_info.get("name")}-peliin, {username}!\n')
        print(f'Pelin säännöt:\n\n{self.game_info.get("rules")})\n')

    # Database related methods
    def create_game_type(self):
        '''
        Creates a new game type in the database. References the class name as the game type name
        '''
        try:
            exists_query = 'SELECT * FROM game_types WHERE name = %s'
            check_existance = self.db.query(exists_query, (self.game_info.get('name'),), cursor_settings={'dictionary': True})
            
            if len(check_existance['result']) > 0:
                return
            
            query = 'INSERT INTO game_types (name, rules) VALUES (%s, %s)'
            values = (self.game_info.get('name'), self.game_info.get('rules'))
            
            self.db.query(query, values)
        except Exception as error:
            logging.error(f'Error creating the game type: {error}')
            return False
    
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
    
    def save_game_to_history(self, win_amount: int, bet: int) -> bool:
        '''
        Saves the game to the database. Returns success state boolean
        '''
        try:
            query = '''
                INSERT INTO game_history
                (bet, win_amount, played_at, user_id, game_type_id)
                VALUES (%s, %s, %s, %s, %s)
            '''
            
            user_id = self.player.get_data().get('id')
            game_type_id = self.db.query('SELECT id FROM game_types WHERE name = %s', (self.game_info.get('name'),), cursor_settings={'dictionary': True})['result'][0].get('id')

            values = (bet, win_amount, datetime.now(), int(user_id), int(game_type_id))
            
            result = self.db.query(query, values)
            
            if result['affected_rows'] > 0:
                return True
            else:
                raise Exception('Unexpected error saving the game')
        except Exception as error:
            logging.error(f'Error saving the game: {error}')
            return False