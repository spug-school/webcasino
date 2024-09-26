from cli.main import Cmd
from config import config

name = r"""
  ____  _      ___    ____     _     ____  ___  _   _   ___
 / ___|| |    |_ _|  / ___|   / \   / ___||_ _|| \ | | / _ \
| |    | |     | |  | |      / _ \  \___ \ | | |  \| || | | |
| |___ | |___  | |  | |___  / ___ \  ___) || | | |\  || |_| |
 \____||_____||___|  \____|/_/   \_\|____/|___||_| \_| \___/
"""

def main()-> None:
    print(name)
    foo = Cmd()
    selectedGame = foo.auth()
    print(selectedGame)
    # print(config())

if __name__ == '__main__':
    main()
