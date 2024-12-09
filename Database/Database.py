import mysql.connector
import logging
import os
from helpers.get_file_path import get_file_path

class Database:
    '''
    Core class for all database related actions
    
    Attributes:
        config (dict): A dictionary containing the database connection parameters
        setup (bool): Whether the database is being set up
        setup_files (list): A list of source (`.sql`) files to run on setup
    '''
    def __init__(self, config: dict, setup: bool = False, setup_files: list | tuple = []):
        self.config = config
        self.connection = self.create_connection(setup)
        
        if setup:
            self._setup_database(config.get('setup_file', None), setup_files)
        
        
    def create_connection(self, setup: bool = False) -> mysql.connector.connection.MySQLConnection:
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
            
            # setting up -> database connection will not work
            # unless the database is created first
            if setup:
                with connection.cursor() as cursor:
                    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.config["db_name"]}')
                    cursor.execute(f'USE {self.config["db_name"]}')
            
            # push the db name to the connection
            connection.database = self.config['db_name']
            
            return connection
        except Exception as error:
            print(error)
            return None
        
    def _setup_database(self, file_name: str, source_files: list = []) -> bool:
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
            return False
        
        try:
            # runs the config-defined setup script
            # -> should be an sql file with the initial db structure
            with open(get_file_path(file_name), 'r', encoding='utf-8') as setup_file:
                setup_script = setup_file.read()
                self._execute_script(setup_script)
            
            # executes runs other source (.sql) files
            for source_file_name in source_files:
                source_file_path = get_file_path(source_file_name)

                if not os.path.exists(source_file_path) or not os.path.isfile(source_file_path):
                    logging.warning(f'File {source_file_name} not found')
                    continue
                if '.sql' not in source_file_name:
                    source_files.remove(source_file_name)
                    continue
                with open(get_file_path(source_file_name), 'r', encoding='utf-8') as source_file:
                    source_script = source_file.read()
                    self._execute_script(source_script)
                    
            print(f'Database setup complete. Sourced files {", ".join(source_files)}')
        except Exception as error:
            logging.error(f'Error setting up the database: {error}')
           
    def _execute_script(self, script: str):
        '''
        Executes a multi-statement SQL script
        '''
        with self.connection.cursor() as cursor:
            sql_statements = script.split(';')
            for statement in sql_statements:
                if statement.strip():
                    cursor.execute(statement)
                    self.commit_changes()

             
    def query(self, query: str, values: tuple = (), cursor_settings: dict = {}) -> dict:
        '''
        Executes singular `query` on the database
        
        Parameters:
            query (str): The query to execute
            values (tuple): The values to pass to the query
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
                'result': data_found if len(data_found) > 0 else [],
            }
        except Exception as error:
            print(error)
            return {
                'affected_rows': 0,
                'result_group': False,
                'result': [],
                'error': str(error)
            }
            
    def commit_changes(self) -> bool:
        self.connection.commit()