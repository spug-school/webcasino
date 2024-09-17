from dotenv import load_dotenv
import os

def config() -> dict:
    load_dotenv()

    return {
        'db_connection': {
            'db_host': os.getenv('DB_HOST'),
            'db_port': os.getenv('DB_PORT'),
            'db_user': os.getenv('DB_USER'),
            'db_pass': os.getenv('DB_PASS'),
            'autocommit': os.getenv('DB_AUTOCOMMIT', False),
            'collation': 'utf8mb4_general_ci',
        }
    }