name = r"""
  ____  _      ___    ____     _     ____  ___  _   _   ___
 / ___|| |    |_ _|  / ___|   / \   / ___||_ _|| \ | | / _ \
| |    | |     | |  | |      / _ \  \___ \ | | |  \| || | | |
| |___ | |___  | |  | |___  / ___ \  ___) || | | |\  || |_| |
 \____||_____||___|  \____|/_/   \_\|____/|___||_| \_| \___/
"""


# helpers
def clear_terminal():
    '''
    Clears the terminal, and prints the logo
    '''
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{name}\n')

def heading(text: str) -> str:
    return f'\n\033[1m{text}\033[0m\n'

def header(text: str, balance: int):
    '''
    Prints the header. Call this on the start of each loop
    '''
    # clear_termginal()
    return print(f'{text}  |  Saldo: {balance}\n\n')
