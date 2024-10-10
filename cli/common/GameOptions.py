from enum import Enum

class GameOption(Enum):
    @classmethod
    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

def create_game_options(game_types):
    # create the game options
    game_types.append((len(game_types) + 1, 'Takaisin', 'BACK'))
    game_options_dict = {name.upper(): id_ for id_, name, name_en in game_types}
    GameOptions = Enum('GameOptions', game_options_dict)

    # create the game classes
    game_classes_dict = {name.upper(): class_name.capitalize() for id, name, class_name in game_types}
    GameClasses = Enum('GameClasses', game_classes_dict)

    return GameOptions, GameClasses

# declare the GameOptions and GameClasses variables with default values
# -> gets updated in the Cmd class
GameOptions, GameClasses = create_game_options([])