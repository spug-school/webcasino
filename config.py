from dotenv import load_dotenv
import os

def config() -> dict:
    load_dotenv()

    return {
        'db_host': os.getenv('DB_HOST'),
        'db_port': os.getenv('DB_PORT'),
        'db_user': os.getenv('DB_USER'),
        'db_pass': os.getenv('DB_PASS'),
        'db_name': os.getenv('DB_NAME', None),
        'autocommit': bool(os.getenv('DB_AUTOCOMMIT', False)),
        'collation': 'utf8mb4_unicode_ci',
        'setup_file': os.getenv('DB_SETUP_FILE', 'setup.sql'),
        'secret_key': os.getenv('API_SECRET_KEY')
    }