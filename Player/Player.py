import hashlib
from Database.Database import Database

class Player:
    '''
    Represents a player from the db, and handles the player's data manipulation.
    The current class is used to update the player's data in the database after/during each singular game.
    '''
    def __init__(self, user_id: int, db_handler: Database):
        self._db = db_handler
        self.id = user_id

        # holds both the user and user_statistics data
        self.data = self._load_data(user_id)

    # ------------------------------
    # Getters
    # ------------------------------
    def get_data(self, with_password: bool = True) -> dict:
        if not with_password:
            data_without_password = self.data.copy()
            del data_without_password['password']
            return data_without_password
        return self.data

    def get_balance(self) -> int:
        return int(self.data.get('balance'))
    
    def get_username(self) -> str:
        return self.data.get('username')

    def get_ban_status(self) -> bool:
        return self.data.get('is_banned')

    # ------------------------------
    # Setters
    # ------------------------------
    def update_total_winning(self, amount: int):
        self.data['total_winnings'] += amount

    def update_games_played(self):
        self.data['games_played'] += 1

    def update_games_won(self):
        self.data['games_won'] += 1

    def update_games_lost(self):
        self.data['games_lost'] += 1

    def update_balance(self, amount: int):
        self.data['balance'] += amount

    def set_banned(self, status: bool):
        self.data['is_banned'] = status
    
    def _load_data(self, user_id: int) -> dict | bool:
        user_query = '''
            SELECT * FROM users
            WHERE id = %s
        '''
        profile_query = '''
            SELECT
                balance,
                total_winnings,
                games_played,
                games_won,
                games_lost,
                is_banned
            FROM user_statistics
            WHERE user_id = %s
        '''

        user_result = self._db.query(user_query, (user_id,), cursor_settings={'dictionary': True})
        user_data = user_result['result'][0]

        profile_result = self._db.query(profile_query, (user_id,), cursor_settings={'dictionary': True})
        profile_data = profile_result['result'][0]
        
        return {**user_data, **profile_data} # Merge user and profile data
    
    def update_username(self, new_name: str) -> bool:
        self.data['username'] = new_name
        return self.save()
        
    def update_password(self, new_password: str):
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.data['password'] = hashed_password
        return self.save()
    
    def unban_account(self, balance_to_set: int) -> bool:
        '''
        Unbans the player's account
        
        Parameters:
            balance_to_set (int): The balance to set for the player
        
        Returns:
            bool: Success state
        '''
        self.set_banned(False)
        self.update_balance(balance_to_set)
        return self.save()
    
    def delete_account(self) -> bool:
        '''
        Deletes the player's user & profile from the database
        
        Returns:
            bool: Success state
        '''
        try:
            user_id = (self.get_data().get('id'),)
            self._db.connection.start_transaction()
            
            # first, delete the user's statistics
            query_stats = '''
                DELETE FROM user_statistics WHERE user_id = %s
            '''
            
            self._db.query(query_stats, user_id)
            
            # then delete the user's game_history
            query_history = '''
                DELETE FROM game_history WHERE user_id = %s
            '''
            self._db.query(query_history, user_id)
            
            # theeen at last delete the user itself
            query_user = '''
                DELETE FROM users WHERE id = %s
            '''
            result = self._db.query(query_user, user_id)
            
            self._db.commit_changes()
            
            if result['affected_rows'] > 0:
                return True
            else:
                return False
        except:
            self._db.connection.rollback() # go back if we encounter an issue
            return False
        
    def save(self) -> bool:
        '''
        Updates the players data in the database tables
        
        TODO - could be optimized to only update the changed values
        '''
        try:
            self._save_credentials()
            self._save_profile()
            self._db.commit_changes()
            return True
        except:
            self._db.connection.rollback()
            return False
        
    def _save_credentials(self):
        '''
        Updates the player's credentials in the database
        '''
        query = '''
            UPDATE users
            SET username = %s, password = %s
            WHERE id = %s
        '''
        
        values = (
            self.data['username'],
            self.data['password'],
            self.data['id']
        )
        
        self._db.query(query, values)
        self._db.connection.commit()
        
    def _save_profile(self):
        '''
        Updates the player's profile in the database
        '''
        query = '''
            UPDATE user_statistics
            SET balance = %s, total_winnings = %s, games_played = %s, games_won = %s, games_lost = %s, is_banned = %s
            WHERE user_id = %s
        '''
        
        values = (
            self.data['balance'],
            self.data['total_winnings'],
            self.data['games_played'],
            self.data['games_won'],
            self.data['games_lost'],
            self.data['is_banned'],
            self.data['id']
        )
        
        self._db.query(query, values)