# -----------------------------------
# Handles the creation of the main
# menu options and the cli view 
# component classes as a part of it.
# -----------------------------------

from enum import Enum
from cli.views.CLIView import CLIView
from cli.views import *

def create_menu_options():
    cli_view_classes = {}
    enum_value = 1
    
    # default game_menu option
    cli_view_classes['PELIVALIKKO'] = (enum_value, None)
    enum_value += 1 
    
    # loop thru all the views imported in cli/views/__init__.py
    for attribute_name in globals().copy():
        attribute = globals()[attribute_name]
        if isinstance(attribute, type) and issubclass(attribute, CLIView) and attribute is not CLIView:
            view_name = '_'.join(attribute.view_name.upper().split())
            cli_view_classes[view_name] = (enum_value, attribute)
            enum_value += 1  # Increment the enum value
    
    # default "back" option
    cli_view_classes['LOPETA'] = (enum_value, None)
    
    return cli_view_classes

menu_options = create_menu_options()
MenuOptions = Enum('MenuOptions', {k: v[0] for k, v in menu_options.items()})
ViewClasses = {k: v[1] for k, v in menu_options.items()}