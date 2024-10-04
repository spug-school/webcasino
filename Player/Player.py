import mysql.connector
import logging
import hashlib

class Player:
    '''
    Holds the player's data in a temporary Class, and handles the player's data manipulation.
    The current class is used to update the player's data in the database after/during each singular game.
    '''
    def __init__(self, username: str, db_handler: object):
        self.__db = db_handler
        self.__data = self.__load_existing(username) if self.__load_existing(username) else self.__create_new(username)

    def get_data(self) -> dict:
        return self.__data
    
    def get_balance(self) -> int:
        '''
        Needed so frequently that it's worth having a separate method for it
        '''
        return self.__data.get('balance')
    
    def get_username(self) -> str:
        '''
        As is this
        '''
        return self.__data.get('username', '')

    def update_total_winning(self, amount: int):
        self.__data['total_winnings'] += amount

    def update_games_played(self):
        self.__data['games_played'] += 1
    
    def update_games_won(self):
        self.__data['games_won'] += 1
    
    def update_games_lost(self):
        self.__data['games_lost'] += 1
    
    def update_balance(self, amount: int):
        self.__data['balance'] += amount
        
    def set_banned(self):
        self.__data['is_banned'] = True
    
    # TODO logic that tracks each game session (start of the game - leaving the game)

    # Db methods
    def __load_existing(self, username: str):
        '''
        Handles loading the player's data from the database, if username matches
        '''
        try:
            result = self.__db.query('SELECT * FROM users WHERE username = %s', (username,), cursor_settings={'dictionary': True})
            result_data = result['result']
            
            if len(result_data) == 0:
                return False
            else:
                return result_data[0] # returns the first row
        except mysql.connector.Error as error:
            logging.error(f'Error loading player {self.__data['id']} data: {error}')
            return False

    def __create_new(self, username: str, password: str = '') -> dict:
        '''
        Handles creating a new player in the database
        '''
        # TODO password handling
        try:
            query = '''
                INSERT INTO users 
                (username, password)
                VALUES (%s, %s)
                '''
            self.__db.query(query, (username, password))
            self.__db.connection.commit()
            logging.info(f'New player {username} created successfully')
            return self.__load_existing(username)
        except mysql.connector.Error as error:
            logging.error(f'Error creating new player {username}: {error}')
            return False
    
    def save(self):
        '''
        Used for saving the player's data from the temp object to the database
        '''
        try:
            query = '''
                UPDATE users 
                SET total_winnings = %s, games_played = %s, games_won = %s, games_lost = %s, balance = %s 
                WHERE username = %s
            '''
            values = (self.__data['total_winnings'], self.__data['games_played'], self.__data['games_won'], self.__data['games_lost'], self.__data['balance'], self.__data['username'])
            
            self.__db.query(query, values)
            self.__db.connection.commit()
            
            logging.info(f'Player {self.__data['id']} data saved successfully')
        except mysql.connector.Error as error:
            logging.error(f'Error saving player {self.__data['id']} data: {error}')
            self.__db.connection.rollback()
            return False