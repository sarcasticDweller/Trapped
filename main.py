# python libraries
import random, math
# project libraries
import ui as ttui
from loon import Loon
import map

#Variable declarations
turns_left=50 #Default is 50
debug = 0
status=4
"""
Status meanings:
0: Time out
1: Dead to non-loon-entity
2: Dead to loon
3: Victory
4: Game playing
"""
#Function declarations

def place_entities_in_rooms(): # shitty, i know. to be rewritten
    player_room=map.rooms[math.floor((len(map.rooms)-1)/2)] # should always be the center of the map
    while True:
        loon_room=map.get_random_room()
        if loon_room!=player_room:
            break
    bats_room=map.get_random_room()
    return player_room, loon_room, bats_room



def detect_entity(reference, target):
    """
    A wrapper for map.get_neighboring_objects_at_range()
    Return value meanings:
    0: same room
    1: 1 room away
    2: 2 rooms away
    ...
    """
    detection_range = 2
    relative_location, distance = map.get_neighboring_objects_at_range(reference, target, detection_range)
    return distance

def get_random_flavor_text():
    statements=["You know he's here somewhere.... ",
                "He's not in this room. ", 
                "I will find him soon. ",
                "If I give up now I'll never escape. "
    ]
    return random.choice(statements)

def print_debug_display():
    # to rewrite
    pass

loon = Loon(random.choice(map.rooms))

# state machine
def intro_screen():
    answer = ttui.show_start_screen(["Yes", "No"])
    if answer == "Yes":
        return True
    else:
        return False

def game_loop(debug = False):
    player_room, loon.room, bats_room = place_entities_in_rooms()

    


def game_over(status): 
    #Prints game-over messages
    ttui.clear_screen()
    if status==0:
        print("You've lost. You are never escaping.\nIt's a matter of time before the loon gets you.")
    if status==1:
        print("Perhaps this is a better way to die\nthan to the loon's jaws.")
    if status==2:
        print("The hunt is over, and you've\ncome out as the prey.")
    if status==3:
        print("You manage to kill the loon.")
        print("Inside his straight jacket you find a key.")
        print("Maybe there's a chance you might leave someday.")
    ttui.wait_for_button_press()
    ttui.clear_screen()

#Main loop
flavor_text = ""
while True:
    # intro screen
    play_game_choice = intro_screen()
    if not play_game_choice:
        ttui.clear_screen()
        quit()
    
    # game setup
    player_room, loon.room, bats_room = place_entities_in_rooms()
    # game loop
    while True:
        if debug==1:
            print_debug_display()
        
        flavor_text = "" # reset flavor text
        
        # tell user about how close the loon is
        loon_distance = detect_entity(player_room, loon.room)
        if loon_distance == 0: # same room, end game
            if loon.mood == "cranky":
                status=2
                break
            else:
                status=3
                break
        elif loon_distance == 1:
            flavor_text += f"He's close.\nHe sounds as if he's {loon.mood}. "
        elif loon_distance == 2:
            flavor_text += "You hear the loon. "
        else:
            flavor_text += get_random_flavor_text()
        
        # tell user if loon has been here
        if player_room in loon.rooms_visited:
            flavor_text += "You see feathers on the floor. "
        
        # bats & movement
        bats_distance = detect_entity(player_room, bats_room)
        if bats_distance == 0:
            # overrides previous flavor-text. should fix
            flavor_text += "You've awakened the bats. "
            player_room=map.get_random_room()
            bats_room=map.get_random_room()
        elif bats_distance == 1:
            flavor_text += "You hear rustling. "
        
        # logic to always run

        # handle the player
        options = map.get_directions_entity_can_move(player_room)
        player_room_selected = ttui.show_ui(player_room, turns_left, flavor_text, options)
        player_room = map.get_room_entity_moved_to(player_room, player_room_selected)

        loon.update()
        if turns_left<1:
            status=0
            break # end game
        else:
            turns_left -= 1
    game_over(status)
