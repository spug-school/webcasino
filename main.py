from Database.Database import Database
from cli.Cmd import Cmd
from config import config
from server import app

def main():
    ui = 'web'
    if ui == 'web':
        app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)
    else:
        Cmd(config())

if __name__ == '__main__':
    main()