class Leaderboard:
    def __init__(self, db_handler, filter_col, sort, limit = 10):
        self.filter_col = filter_col
        self.sort = sort
        self.limit = limit
        self.db_handler = db_handler

    def get_leaderboard(self):
        query = f'''
                SELECT 
                u.username as 'käyttäjänimi',
                s.total_winnings as 'kokonaisvoitot',
                s.games_played as 'pelejä pelattu',
                s.games_won as 'pelejä voitettu',
                s.games_lost as 'pelejä hävitty'
            FROM users u
            JOIN user_statistics s
            ON u.id = s.user_id
            WHERE u.hidden = 0
            ORDER BY {self.filter_col} {self.sort}
            LIMIT {self.limit}
        '''
        
        result = self.db_handler.query(query, cursor_settings={'dictionary': True})
        
        return result['result']