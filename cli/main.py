import argparse

from Database.Database import Database
from config import config

class Cmd:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="CLI CASINO")
        self.parser.add_argument(
            '--version',
            action='version',
            version='CLI Casino 1.0'
        )
        self.parser.add_argument(
            '--game',
            help='Game list [blackjack, roulette, dice]'
        )
        self.parser.add_argument(
            '--auth',
            help='Create an account'
        )
        self.parser.add_argument(
            '--balance',
            help='my current balance'
        )

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
        username = auth.split(' ')[1]
        password = auth.split(' ')[2]
        db = Database(**config())
        user = db.query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        if not user:
            return 'Invalid credentials'

        return f'Welcome {username}'

    def _register(self) -> str:
        print('Create an account')
        username = input('Enter username: ')
        password = input('Enter password: ')
        db = Database(**config())
        db.query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        return f'Username: {username}\nPassword: {password}'

    def balance(self) -> str:
        return self.parser.parse_args().balance

    def parse_args(self) -> argparse.Namespace:
        return self.parser.parse_args()
