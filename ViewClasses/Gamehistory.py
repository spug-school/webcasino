class Gamehistory:
    def __init__(self, db_handler, user_id, limit = 10):
        self.user_id = user_id
        self.limit = limit
        self.db_handler = db_handler
        
    def get_gamehistory(self):
        query = f'''
            SELECT
                game_history.bet,
                game_history.win_amount,
                game_history.played_at,
                game_types.name
            FROM game_history
            JOIN game_types
            ON game_history.game_type_id = game_types.id
            WHERE game_history.user_id = {self.user_id}
            ORDER BY game_history.played_at DESC
            LIMIT 10
        '''
        
        result = self.db_handler.query(query, cursor_settings={'dictionary': True})
        
        return result['result']