from enum import Enum

class GameOption(Enum):
    @classmethod
    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

def create_game_options(game_types):
    game_types.append((len(game_types) + 1, 'Takaisin', 'BACK'))
    game_options_dict = {name.upper(): id_ for id_, name, name_en in game_types}
    GameOptions = Enum('GameOptions', game_options_dict)
    return GameOptions

# declare the GameOptions variable with a default value
# -> gets updated in the Cmd class
GameOptions = create_game_options([])