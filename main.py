from Database.Database import Database
from cli.Cmd import Cmd
from config import config

def main():
    # CMD supports the following arguments:
    # --auth: Sign in or sign up to the casino
    # --setup: Start the casino with the db setup for the database (for first time startup)
    #
    # Example usage:
    # python main.py --auth "signup foo bar"
    # python main.py --auth "signin foo bar" --setup
    
    cmd = Cmd(config())
    print(cmd)

if __name__ == '__main__':
    main()
