import mysql.connector
import logging

class Player:
    '''
    Holds the player's data in a temporary Class, and handles the player's data manipulation.
    The current class is used to update the player's data in the database after/during each singular game.
    '''
    def __init__(self, username: str, db_handler: object, player: dict = None):
        self.__db = db_handler
        self.__data = player if player else self.__load_existing(username)

    def get_data(self) -> dict:
        return self.__data

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
    
    # TODO logic that tracks each game session (start of the game - leaving the game)

    # Db methods
    def __load_existing(self, username: str) -> dict|None:
        try:
            result = self.__db.query('SELECT * FROM users WHERE username = %s', (username,), cursor_settings={'dictionary': True})
            return result[0] if result else None
        except mysql.connector.Error as error:
            logging.error(f'Error loading player {self.__data.get('id')} data: {error}')
            return None

    def save(self):
        try:
            self.__db.query('UPDATE users SET total_winnings = %s, games_played = %s, games_won = %s, games_lost = %s, balance = %s WHERE username = %s', (self.__data['total_winnings'], self.__data['games_played'], self.__data['games_won'], self.__data['games_lost'], self.__data['balance'], self.__data['username']))
            self.__db.connection.commit()
        except mysql.connector.Error as error:
            print(f'Error saving player {self.__data.get('id')} data: {error}')
            return False