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

def push_to_display(line_one, line_two = ""): 
    print(f"{line_one}\n{line_two}")

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
    push_to_display("Press any key to continue")
    input()

def list_menu(prompt = "", options = []):
    '''
    Takes a list

    :param prompt: Description of menu
    :param options: Menu items
    :return: Returns option selected
    Returns an item from a list provided
    '''

    # insert visual end-of-arrays
    options.insert(0, "<|") # low boundary
    options.append("|>") # high boundary
    option_selected = 0
    while True:
        push_to_display(prompt, f"<< {options[option_selected]} >>")
        button_pressed = int(input())
        if button_pressed == 2:
            if option_selected != 0 and option_selected != len(options) - 1: 
                return options[option_selected]
        if button_pressed == 1:
            if option_selected > 0:
                option_selected -= 1
        elif button_pressed == 3:
            if option_selected < len(options) - 1:
                option_selected += 1


def show_stat_screen(player_room, turns_left):
    lines()
    print("Room      : " + str(player_room))
    print("Turns left: " + str(turns_left))
    lines()