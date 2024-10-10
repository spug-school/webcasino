import logging, time, sys
from typing import override
from cli.views.CLIView import CLIView
from cli.common.utils import clear_terminal

class PlayerProfile(CLIView):
    view_name = 'Profiili'
    
    def __init__(self, db_handler: object, player: object):
        super().__init__(db_handler, player, self.view_name)
        
        # View specific attributes
        self._profile_menu = [
            {'Omat statistiikat': None},
            {'Muuta käyttäjätietoja': (
                'Vaihda käyttäjänimi',
                'Vaihda salasana',
                'Kumoa porttikielto',
                'Poista käyttäjä',
                'Takaisin',
            )}, # self._profile_update_menu
            {'Takaisin': None},
        ]
        
    def _display_profile_menu(self):
        profile_menu_keys = [list(menu.keys())[0] for menu in self._profile_menu]
    
        return self.sub_menu(profile_menu_keys, f'Valitse toiminto (1 - {len(self._profile_menu)}): ')
    
    def __get_stats(self) -> list:
        '''
        Gets the player statistics from the user_statistics table
        '''
        try:
            query = f'''
                SELECT
                    user_statistics.total_winnings as 'Kokonaisvoitot (pisteet)',
                    user_statistics.games_played as 'Pelatut pelit',
                    user_statistics.games_won as 'Voitetut pelit',
                    user_statistics.games_lost as 'Hävityt pelit',
                    CASE
                        WHEN user_statistics.is_banned = 0 THEN 'Ei'
                        WHEN user_statistics.is_banned = 1 THEN 'Kyllä'
                    END as 'Porttikiellossa'
                FROM user_statistics
                WHERE user_id = {self.player.get_data().get('id')}
            '''
            
            result = self.db.query(query, cursor_settings={'dictionary': True})
            
            if result['result_group']:
                return result['result']
            else: # practically cant happen since there is atleast the default data
                return []
        except Exception as error:
            logging.error(f'Error getting the player stats: {error}')
            return []
    
    def _show_stats(self, data: list = []):
        '''
        Prints the player statistics in a table
        '''
        self.show_header(text = 'Omat tilastot')
        
        headers = data[0].keys()
        rows = [list(row.values()) for row in data]
        
        alignment = ['center'] * len(headers)
        
        self.display_table(rows, headers, alignment)
    
    @override
    def view(self) -> bool:
        '''
        View-specific logic: PlayerProfile
        '''
        while True:
            self.show_header()
            
            profile_menu_choice = self._display_profile_menu()
            
            match profile_menu_choice:
                case 1: # show stats
                    self.show_header(text = 'Omat statistiikat')
                    self._show_stats(self.__get_stats())
                    
                    input('\nPalaa takaisin painamalla <Enter>\n')
                    continue
                case 2: # profile actions
                    while True:
                        self.show_header(text = 'Muuta käyttäjätietoja')
                        
                        action_choice = self.sub_menu(list(self._profile_menu[1].values())[0], f'Valitse toiminto (1 - {len(self._profile_menu[1])}): ')
                        
                        match action_choice:
                            case 1:
                                self.show_header(text = 'Vaihda käyttäjänimi')
                                
                                new_name = self.validate_input('Syötä uusi käyttäjänimi (syötä tyhjä peruuttaaksesi): ', 'str', allow_empty = True, sanitize = True)

                                if not new_name:
                                    continue
                                
                                if self.player.update_username(new_name):
                                    print('Käyttäjänimi vaihdettu.\n')
                                    self.player.save()
                                    time.sleep(2)
                                else:
                                    print('Käyttäjänimen vaihto epäonnistui.\n')
                                    time.sleep(2)
                            case 2:
                                self.show_header(text = 'Vaihda salasana')
                                
                                new_password = self.validate_input('Syötä uusi salasana (syötä tyhjä peruuttaaksesi): ', 'str', allow_empty = False, sanitize = True)
                                
                                if not new_password:
                                    continue
                                
                                if self.player.update_password(new_password):
                                    print('Salasana vaihdettu.\n')
                                    self.player.save()
                                    time.sleep(2)
                                else:
                                    print('Salasanan vaihto epäonnistui.\n')
                                    time.sleep(2)
                            case 3:
                                self.show_header(text = 'Kumoa porttikielto')
                                
                                if self.player.get_ban_status() == 1:
                                    balance_to_return = self.validate_input('Syötä palautettava saldo (max. 1000): ', 'int', 1, 1000)
                                    
                                    if self.player.unban_account(balance_to_return):
                                        print(f'Porttikielto poistettu. Saldoa lisätty {balance_to_return}\n')
                                        self.player.save()
                                    else:
                                        print('Porttikiellon poisto epäonnistui.\n')
                                        time.sleep(1)
                                else:
                                    print('Et ole porttikiellossa!\n')
                                    time.sleep(2)
                            case 4:
                                self.show_header(text = 'Poista käyttäjä')
                                
                                confirm = self.validate_input('Haluatko varmasti poistaa käyttäjän? (k / e): ', 'str', allowed_values = ('k', 'e'))
                                
                                if confirm == 'k':
                                    if self.player.delete_account():
                                        clear_terminal()
                                        print('\nKäyttäjä poistettu.\n')
                                        print('Kiitos peliemme pelaamisesta!\n')
                                        time.sleep(1)
                                        sys.exit() # just close the program, we dont allow unauthorized access
                                    else:
                                        print('\nKäyttäjä ei poistettu.\n')
                                        time.sleep(2)
                                else:
                                    print('\nKäyttäjää ei poistettu.\n')
                                    time.sleep(2)
                            case 5:
                                break
                            case _ if action_choice == len(self._profile_menu):
                                self.player.save()
                                break
                            case _:
                                print(f'Virheellinen valinta! Valitse numerolla 1 - {len(self._profile_update_menu)}\n')
                case _ if profile_menu_choice == len(self._profile_menu):
                    break
                case _:
                    print(f'Virheellinen valinta! Valitse numerolla 1 - {len(self._profile_menu)}\n')
            
            return True