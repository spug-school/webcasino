import logging
from typing import override
from cli.views.CLIView import CLIView
from cli.common.utils import header

class Leaderboard(CLIView):
    view_name = 'Tulostaulut'
    
    def __init__(self, db_handler: object, player: object):
        super().__init__(db_handler, player, self.view_name)
        
        # View specific attributes
        self.leaderboard_rows = 10  
        self.filter_options = [
            {'db_column': 'total_winnings', 'title': 'Kokonaisvoitot (pisteet)'},
            {'db_column': 'games_played', 'title': 'Pelatut pelit'},
            {'db_column': 'games_won', 'title': 'Voitetut pelit'},
            {'db_column': 'games_lost', 'title': 'Hävityt pelit'},
            {'db_column': None, 'title': 'Takaisin'}
        ]
        self.sort_options = [
            {'order': 'DESC', 'title': 'Laskeva'},
            {'order': 'ASC', 'title': 'Nouseva'}
        ]
    
    def _get_filtered_data(self, filter_column: str, sort: str = 'DESC'):
        '''
        Executes the query to get the filtered data from the db based on the user's choice
        '''
        try:
            query = f'''
                SELECT 
                    users.username,
                    user_statistics.total_winnings,
                    user_statistics.games_played,
                    user_statistics.games_won,
                    user_statistics.games_lost
                FROM users
                JOIN user_statistics
                ON users.id = user_statistics.user_id
                ORDER BY {filter_column} {sort}
                LIMIT {self.leaderboard_rows}
            ''' 
            
            result = self.db.query(query, cursor_settings={'dictionary': True})
            
            if result['result_group']: # if there are results
                return result['result']
        except Exception as error:
            logging.error(f'Error getting the filtered leaderboard: {error}')
            return []
                
    def _print_table(self, data: list, filter: str, sort_order: str = 'DESC') -> None:
        '''
        Prints the leaderboard table
        '''
        self.show_header(text = 'Taulukko')

        headers = ['#', 'Käyttäjänimi'] + [option['title'] for option in self.filter_options if option['db_column']] + ['Voitto-%']
        rows = []
        
        for index, row in enumerate(data, start = 1):
            win_percentage = (row['games_won'] / row['games_played'] * 100) if row['games_played'] > 0 else 0
            win_percentage = min(win_percentage, 100) # cap the win percentage to 100
            rows.append([index] + list(row.values()) + [f"{win_percentage:.2f}%"])
        
        alignment = ['center', 'left'] + ['center'] * (len(headers) - 2)
        
        table_description = f'10 parasta pelaajaa "{filter}" mukaan {"laskevassa" if sort_order == "DESC" else "nousevassa"} järjestyksessä'
        self.display_table(rows, headers, alignment, table_description)
        
    @override
    def view(self) -> bool:
        '''
        View-specific logic: Leaderboard
        '''
        self.show_header(text = 'Järjestyskriteeri')
        
        print('Valitse haluamasi järjestyskriteeri:\n')
        filter_choice = self.sub_menu([option['title'] for option in self.filter_options])

        if filter_choice == len(self.filter_options): # back to main menu
            return False
        
        filter_column = self.filter_options[filter_choice - 1].get('db_column')
        
        self.show_header(text = 'Järjestys')
        
        print('Valitse järjestys:\n')
        sort_choice = self.sub_menu([option['title'] for option in self.sort_options], False)
        
        if not sort_choice:
            return False
        
        data = self._get_filtered_data(filter_column, self.sort_options[sort_choice - 1].get('order', 'DESC'))  
        self._print_table(data, self.filter_options[filter_choice - 1].get('title'), sort_choice)
        
        input('\nPalaa takaisin painamalla <Enter>\n')
            
        return True