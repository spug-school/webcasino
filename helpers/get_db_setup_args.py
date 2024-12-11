import argparse

def get_db_setup_args() -> bool:
    '''
    Parses the command line arguments to determine if the database should be setup
    and to get the list of setup files.
    
    Returns:
        Tuple[bool, List[str]]: A tuple containing the setup flag and the list of setup files
    '''
    parser = argparse.ArgumentParser(description='Setup the database')
    parser.add_argument('--setup', action='store_true', help='Setup the database')
    parser.add_argument('--files', nargs='*', default=[], help='List of setup files')
    args = parser.parse_args()
    
    return args.setup, args.files