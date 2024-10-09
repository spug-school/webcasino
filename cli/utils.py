import shutil

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

def header(text: str, balance: int = 0, clear: bool = True, hide_balance: bool = False) -> None:
    '''
    Prints the header. Call this on the start of each loop
    '''
    if clear:
        clear_terminal()
    return print(f'{text}  {f"|  Saldo: {balance}" if not hide_balance else ''}\n\n')

def fetch_game_types(db: object) -> list:
    '''
    Gets the game type records from the db as a list
    '''
    try:
        result = db.query('SELECT * FROM game_types', cursor_settings={'dictionary': True})
        
        if result['result_group']:
            game_types = [(game['id'], game['name'].capitalize(), game['name_en'].upper()) for game in result['result']]
            return game_types
        else:
            return []
    except Exception as error:
        return []
    
def get_prompt(prompt: str, start: str, end: str, values: tuple = (), is_numeric: bool = True) -> str:
    '''
    Gets the user's choice validated
    '''
    while True:
        choice = input(prompt)
        if is_numeric:
            if choice.isnumeric():
                if int(choice) >= int(start) and int(choice) <= int(end):
                    return int(choice)
                else:
                    print(f'Virheellinen syöte. Syötä numero {start} - {end}')
            else:
                print(f'Virheellinen syöte. Syötä numero {start} - {end}')
        else:
            if choice in values:
                return choice
            else:
                print(f'Virheellinen syöte. Syötä {" / ".join(values)}')
                
def box_wrapper(text: str, min_width: int = 75, max_width: int = 75):
    '''
    Creates a nice box-like wrapper for a wanted text.
    Used in displaying the game rules, for example
    
    Could be located elsewhere tho - TODO
    '''
    terminal_width = shutil.get_terminal_size().columns
    padding = 4 # padding on both sides
    
    # fix the max width to the terminal width
    if terminal_width < max_width:
        max_width = terminal_width - padding
    
    paragraphs = text.split('\n')
    wrapped_lines = []

    for paragraph in paragraphs:
        words = paragraph.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += (word + " ")
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        wrapped_lines.append(current_line.strip())

    # determine the width of the box
    box_width = max(max(len(line) for line in wrapped_lines) + padding, min_width)

    print('+' + '-' * box_width + '+')

    for line in wrapped_lines:
        print(f'| {line.ljust(box_width - padding//2)} |')

    print('+' + '-' * box_width + '+\n')