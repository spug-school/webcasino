import hashlib
from Database.Database import Database

class Auth:
    def __init__(self, db_handler: Database):
        self._db = db_handler

    def create_user(self, username: str, password: str):
        try:
            # create the user first
            user_query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
            hashed_password = self._hash_password(password)
            self._db.query(user_query, (username, hashed_password))

            # grab the created user's id
            created_user_id = self._db.query('SELECT LAST_INSERT_ID() AS id')['result'][0][0]
            
            # create the "profile" after the user is created
            profile_query = 'INSERT INTO user_statistics (user_id) VALUES (%s)'
            self._db.query(profile_query, (created_user_id,))

            return created_user_id
        except Exception as error:
            print(error)
        
    def login(self, username: str, password: str):
        user_exists_query = 'SELECT id FROM users WHERE username = %s'
        user_exists_result = self._db.query(user_exists_query, (username,))
        
        if not user_exists_result['result_group']:
            return False

        # authenticate user
        auth_query = '''
            SELECT id
            FROM users
            WHERE username = %s AND password = %s
        '''
        hashed_password = self._hash_password(password)
        auth_result = self._db.query(auth_query, (username, hashed_password), cursor_settings={'dictionary': True})

        # user found
        if auth_result['result_group']:
            user_id = auth_result['result'][0]['id']
            return user_id

        return False
        
    def user_exists(self, username: str) -> bool:
        query = 'SELECT id FROM users WHERE username = %s'
        result = self._db.query(query, (username,))
        return result['result_group']

    def _hash_password(self, password: str) -> str:
        '''
        Hashes the password using SHA256 (just mock, this is NOT safe)
        '''
        return hashlib.sha256(password.encode()).hexdigest()