import mysql.connector
import logging
from helpers.get_file_path import get_file_path
from cli.common.utils import box_wrapper

class Database:
    '''
    Core class for all database related actions
    
    Attributes:
        config (dict): A dictionary containing the database connection parameters
        connect (bool): Whether to connect to the db
        setup (list): A list of setup/source files
    '''
    def __init__(self, config: dict, connect: bool = True, setup: list = None):
        self.config = config
        self.setup_file = config.get('setup_file')
        self.connection = self.create_connection(setup = True if setup else False) if connect else None
        
        if setup:
            self.setup_database(
                file_name = self.setup_file,
                source_files = setup
            )
        
    def create_connection(self, setup: bool = False) -> mysql.connector.connection.MySQLConnection:
        '''
        Creates a connection to the db, and returns the connection object
        
        Parameters:
            setup (bool): Whether to setup the db
        
        Returns:
            mysql.connector.connection.MySQLConnection: The connection object
        '''
        try: 
            connection = mysql.connector.connect(
                host = self.config['db_host'],
                port = self.config['db_port'],
                user = self.config['db_user'],
                password = self.config['db_pass'],
                autocommit = self.config['autocommit'],
                collation = self.config['collation'],
                charset = 'utf8mb4'
            )

            if setup:
                # create the database if it doesn't exist
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.config['db_name']}`")
                cursor.close()
            
            # Reconnect to the newly created database
            connection.database = self.config['db_name']

            logging.info(f'Connected to database `{connection.database}`')
            return connection
        except mysql.connector.Error as connection_error:
            logging.error(f'Error connecting to the database: {connection_error}')
            return None
    
    def close_connection(self) -> bool:
        '''
        Closes the connection to the db
        
        Returns:
            bool: Success state
        '''
        try:
            self.connection.commit()  # Commit any pending transactions
            self.connection.close()
            logging.info('Database connection closed')
            return True
        except Exception as error:
            logging.error(f'Error closing the database connection:\n{error}')
            return False
        
    def setup_database(self, file_name: str, source_files: list = []) -> bool:
        '''
        Runs the initial setup script for the db
        
        Parameters:
            file_name (str): The name of the setup file
            source_files (list): A list of source data files to insert
            
        Returns:
            bool: Success state
        '''
        if file_name is None or file_name == '':
            logging.warning('No setup file provided')
            print('No setup file provided')
            return False
        
        try:
            with open(get_file_path(file_name), 'r', encoding='utf-8') as setup_file:
                setup_script = setup_file.read()
                self.execute_script(setup_script)

            tables = [table[0] for table in self.query("SHOW TABLES")['result']]
            
            # Insert test data if provided
            for source_file_name in source_files:
                with open(get_file_path(source_file_name), 'r', encoding='utf-8') as source_file:
                    source_script = source_file.read()
                    self.execute_script(source_script)

            logging.info(f'Database `{self.connection.database}` setup successfully.\nTables: {tables}')
            print('\n')
            box_wrapper(f'Database `{self.connection.database}` setup successfully.\nTables: {tables}')

            if source_files:
                logging.info(f'Source data inserted successfully')
                box_wrapper(f'Source data inserted successfully')
    
            return True
        except Exception as error:
            logging.error(f'Error setting up the database:\n{error}')
            return False
           
    def execute_script(self, script: str) -> bool:
        '''
        Executes a multi-statement SQL script
        
        Parameters:
            script (str): The script to execute
            
        Returns:
            bool: Success state
        '''
        try:
            with self.connection.cursor() as cursor:
                sql_statements = script.split(';')
                for statement in sql_statements:
                    if statement.strip():
                        cursor.execute(statement)
                        self.connection.commit()
                        
            return True
        except Exception as error:
            logging.error(f'Error executing script:\n{error}')
            return False
             
    def query(self, query: str, values: tuple = (), fetch: bool = True, cursor_settings: dict = {}) -> dict:
        '''
        Executes singular `query` on the database
        
        Parameters:
            query (str): The query to execute
            values (tuple): The values to pass to the query
            fetch (bool): Whether to fetch the results
            cursor_settings (dict): Optional settings for the cursor
            
        Returns:
            dict: A dictionary containing the query results
        '''
        try:
            cursor = self.connection.cursor(**cursor_settings)
            cursor.execute(query, values)
            
            data_found = cursor.fetchall()
            
            return {
                'affected_rows': cursor.rowcount,
                'result_group': True if len(data_found) > 0 else False,
                'result': data_found,
            }
        except Exception as error:
            logging.error(f'Error executing query `{query}`:\n{error}')
            return {
                'affected_rows': 0,
                'result_group': False,
                'result': [],
            }