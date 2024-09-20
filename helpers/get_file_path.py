import os

def get_file_path(filename: str) -> str:
    '''
    Returns the full path of *filename* searched through the whole project directory
    '''
    
    if filename == "" or not isinstance(filename, str):
        return ""
    
    directory = os.path.dirname(os.path.abspath(__file__))
    
    while directory:
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        
        parent_directory = os.path.dirname(directory)
        if parent_directory == directory:
            break
        directory = parent_directory
    
    raise FileNotFoundError(f"{filename} not found in directory {directory} or any of its parent directories")