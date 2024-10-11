from Database.Database import Database
from cli.Cmd import Cmd
from config import config

def main():
    Cmd(config())

if __name__ == '__main__':
    main()