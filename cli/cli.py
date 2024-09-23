import argparse

class CliTool:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='CLI Casino')
        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        self.parser.add_argument('--game', help='Game list [blackjack, roulette, dice]', required=True)
        self.parser.add_argument('--signup', help='Create an account', required=True)
        self.parser.add_argument('--signin', help='Sign into your account', required=True)
        self.parser.add_argument('--balance', help='my current balance', required=True)
