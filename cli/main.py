import argparse

from Database.Database import Database
from config import config

class Cmd:
    def __init__(self, db) -> None:
        self.db = db
        self.parser = argparse.ArgumentParser(description="CLI CASINO")
        self.parser.add_argument(
            '--version',
            action='version',
            version='CLI Casino 1.0'
        )
        self.parser.add_argument(
            '--auth',
            help='Sign in or sign up to the casino'
        )

    def run(self) -> str | None:
        args = self.parser.parse_args()

        if args.auth:
            return self.auth()
        else:
            return self.parser.print_help()

    def auth(self) -> str:
        match self.parser.parse_args().auth.split(' ')[0]:
            case 'signup':
                return self._register()
            case 'signin':
                return self._signin()
            case _:
                return 'Invalid argument'

    def _signin(self) -> str:
        auth = self.parser.parse_args().auth
        if len(auth.split(' ')) == 3:
            username = auth.split(' ')[1]
            password = auth.split(' ')[2]
        else:
            username = input('Enter username: ')
            password = input('Enter password: ')
        db = self.db
        user = db.query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")

        if user.get('result') == []:
            return 'Invalid credentials'

        return f'Welcome {username}'

    def _register(self) -> str:
        print('Create an account')
        username = input('Enter username: ')
        password = input('Enter password: ')
        db = self.db
        user = db.query(f"SELECT username FROM users WHERE username = '{username}'")
        if user.get('result')[0][0] == username:
            return 'User already exists'
        db.query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        return f'Username: {username}\nPassword: {password}'

    def parse_args(self) -> argparse.Namespace:
        return self.parser.parse_args()
