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

    # Getters
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
    
    def get_ban_status(self) -> bool:
        return self.__data.get('is_banned')

    # Setters
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

    # Db methods
    def __load_existing(self, username: str):
        '''
        Handles loading the player's data from the database, if username matches
        '''
        try:
            user_query = 'SELECT * FROM users WHERE username = %s'
            profile_query = 'SELECT * FROM user_statistics WHERE user_id = %s'
            
            user_result = self.__db.query(user_query, (username,), cursor_settings={'dictionary': True})
            user_data = user_result['result']
            
            if len(user_data) == 0:
                return False
            else:
                user_data = user_data[0]
                profile_result = self.__db.query(profile_query, (user_data['id'],), cursor_settings={'dictionary': True})
                profile_data = profile_result['result'][0]
                
                return {**user_data, **profile_data} # Merge user and profile data
        except mysql.connector.Error as error:
            logging.error(f'Error loading player {username} data: {error}')
            return False

    def __create_new(self, username: str, password: str = '') -> dict:
        '''
        Handles creating a new player in the database
        '''
        # TODO password handling
        try:
            user_query = '''
                INSERT INTO users 
                (username, password)
                VALUES (%s, %s)
            '''
            
            self.__db.query(user_query, (username, password))
            self.__db.connection.commit()
            
            user_id = self.__db.query('SELECT LAST_INSERT_ID()')['result'][0][0]
            
            profile_query = '''
                INSERT INTO user_statistics 
                (user_id)
                VALUES (%s)
                '''

            self.__db.query(profile_query, (user_id,))
            self.__db.connection.commit()
            
            logging.info(f'New player `{username}`, id:`{user_id}` created successfully')
            return self.__load_existing(username)
        except mysql.connector.Error as error:
            logging.error(f'Error creating new player {username}: {error}')
            return False
    
    def save(self):
        '''
        Used for saving the player's data from the temp object to the database
        '''
        try:
            user_query = '''
                UPDATE users 
                SET username = %s, password = %s
                WHERE id = %s
            '''
            
            profile_query = '''
                UPDATE user_statistics 
                SET balance = %s, total_winnings = %s, games_played = %s, games_won = %s, games_lost = %s, is_banned = %s
                WHERE user_id = %s
            '''
            
            user_values = (
                self.__data['username'],
                self.__data['password'],
                self.__data['id']
            )
            
            profile_values = (
                self.__data['balance'],
                self.__data['total_winnings'],
                self.__data['games_played'],
                self.__data['games_won'],
                self.__data['games_lost'],
                self.__data['is_banned'],
                self.__data['id']
            )
            
            self.__db.query(user_query, user_values)
            self.__db.query(profile_query, profile_values)
            self.__db.connection.commit()
            
            logging.info(f'Player {self.__data["id"]} data saved successfully')
        except mysql.connector.Error as error:
            logging.error(f'Error saving player {self.__data["id"]} data: {error}')
            self.__db.connection.rollback()
            return False