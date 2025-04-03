# A unified input system
# Some code borrowed from https://github.com/sarcasticDweller/Hanatokei/blob/main/ui.py
import os

print("""==============================
Thank you for using the UI module.
In this current state, the module uses number keys to simulate button presses, as detailed here:
- Left: 1
- Right: 3
- Enter: 2
==============================
""")

left = 1
right = 3
enter = 2

def lines():
    print("//////////////////////////////////")

def clear_screen():
    # clears the screen
    try:
        # assuming we're running a linux/mac
        os.system("clear")
    except:
        # we must be on windows
        os.system("cls")
        # honestly, there could be other errors that arise from this, but as far as try/except blocks go this is the least sinful one in this project

def wait_for_button_press():
    '''
    Waits for a button press
    '''
    print("Press any key to continue")
    input()

def new_list_menu(options, option_selected):
    option_to_return = None

    # ends of arrays
    left_end_cap_index = 0
    right_end_cap_index = len(options) - 1

    print(f"<< {options[option_selected]} >>")
    button_pressed = int(input())
    if button_pressed == enter:
        option_to_return = options[option_selected]
    elif button_pressed == left:
        if option_selected > left_end_cap_index:
            option_selected -= 1
    elif button_pressed == right:
        if option_selected < right_end_cap_index:
            option_selected += 1
    return (option_selected, option_to_return)

def show_ui(player_room, turns_left, flavor_text, options):
    """
    This does two things:
    1. Show's the user information
    2. Take's user's input
    """
    option_cursor_on = 0
    while True:
        clear_screen()
        print("////////////////////")
        print(f"Room       : {player_room}")
        print(f"Turns left : {turns_left}")
        print("====================")
        print(flavor_text)
        print("////////////////////")
        option_cursor_on, direction_to_go = new_list_menu(options, option_cursor_on)
        if direction_to_go != None:
            return direction_to_go

def show_start_screen(options):
    """
    This does two things:
    1. Show's the user information
    2. Take's user's input
    """
    option_cursor_on = 0
    while True:
        clear_screen()
        print("////////////////////")
        print("     Trapped")
        print("====================")
        print("  Play the game?")
        print("////////////////////")
        option_cursor_on, option_picked = new_list_menu(options, option_cursor_on)
        if option_picked != None:
            return option_picked