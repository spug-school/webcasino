from Database.Database import Database
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
    db_configs = config()
    db = Database(
        config = db_configs,
        connect = True,
        setup = False
    )
    cmd = Cmd(db).auth()
    print(cmd)

if __name__ == '__main__':
    main()
