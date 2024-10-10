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
    
def get_prompt(prompt: str, input_type: str = 'str', min_value: int = None, max_value: int = None, allowed_values: tuple = None, allow_empty: bool = False, sanitize: bool = False) -> str | int | None:
    '''
    Validates / sanitizes the input based on the type and constraints provided.
    
    Parameters:
    - prompt (str): The prompt to display to the user.
    - input_type (str): The type of input expected ('str' or 'int').
    - min_value (int): The minimum value for integer inputs.
    - max_value (int): The maximum value for integer inputs.
    - allowed_values (tuple): A tuple of allowed values for string inputs.
    - allow_empty (bool): Whether to allow empty inputs.
    - sanitize (bool): Whether to sanitize the input by removing blacklisted characters.
    
    Returns:
    - str | int | None: The validated and/or sanitized input.
    '''
    blacklisted_chars = [
        ';', 
        '"', 
        "'", 
        ' '
    ]
    
    while True:
        input_value = input(prompt)
        
        if allow_empty and (input_value == '' or input_value.isspace()):
            return None
        
        if input_type == 'int':
            try:
                value = int(input_value)
                if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                    print(f'\nArvon on oltava {min_value} - {max_value}!\n')
                else:
                    return value
            except ValueError:
                print('\nVirheellinen syöte! Syötä numero!\n')
        
        elif input_type == 'str':
            if allowed_values and input_value.lower() not in allowed_values:
                print(f'\nValinnan on oltava {"/".join(allowed_values)}.')
            else:
                if sanitize:
                    return ''.join(char for char in input_value if char not in blacklisted_chars) # don't lower a sanitized input
                else:
                    return input_value.lower()
            
        else:
            print('Syötteen tyyppi on virheellinen.\n')
                
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