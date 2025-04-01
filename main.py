# python libraries
import random, os, math
# project libraries
import ui as ttui
import map

moods=["cranky", "mellow", "asleep"]
"""
cranky: lethal & mobile
mellow: passive & mobile
asleep: passive & immobile
"""

choices=[] # possibly useless?

# variable declarations
player_room = 0
loon_room = 0
bats_room = 0 
loon_room_prev=loon_room
turns_not_moving=0
loon_mood=random.choice(moods)
#Variable declarations
turns_left=50 #Default is 50
debug = 1
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

def place_entities_in_rooms():
    player_room=map.rooms[math.floor((len(map.rooms)-1)/2)] # should always be 12
    print(player_room)
    while True:
        loon_room=map.get_random_room()
        loon_room_prev = loon_room
        if loon_room!=player_room:
            break
    bats_room=map.get_random_room()
    return player_room, loon_room, bats_room

def moveRoom():
    #Moves the player since it doesn't work well in the main loop
    #global player_room #Prevents an error. :/
    #Because borders freak Python out this is here.

    options = map.get_directions_entity_can_move(player_room)
    direction_chosen = ttui.list_menu("Which way would you like to go?", options)
    player_room = map.get_room_entity_moved_to(player_room, direction_chosen)

def detectLoon(): # detects *distance* from player
    """
    Return value meanings:
    0: same room
    1: 1 room away
    2: 2 rooms away
    ...
    """
    proximity_code = 0
    detection_range = 2
    relative_location, distance = map.get_neighboring_objects_at_range(player_room, loon_room, detection_range)
    return distance

def detectBats():
    """
    Return value meanings:
    0: same room
    1: 1 room away
    2: 2 rooms away
    ...
    """
    detection_range = 2
    relative_location, distance = map.get_neighboring_objects_at_range(player_room, bats_room, detection_range)
    return distance

def get_random_flavor_text():
    statements=["You know he's here somewhere...",
                "He's not in this room.", 
                "I will find him soon.",
                "If I give up now I'll never escape."
    ]
    return random.choice(statements)

def loonMood():
    #Handles the randomization of the loon's mood.
    #global loon_mood
    if turns_left%2==0:
        loon_mood=moods[random.randint(0, len(moods)-1)]

def moveLoon(): 
    #global loon_room       # oh
    #global loon_room_prev  # my
    #global turns_not_moving# why
    loon_room_prev=loon_room
    if loon_mood!=moods[2]:
        #Generates choices
        choices = map.get_directions_entity_can_move(loon_room)
        #Loon picks a room
        loon_room_picked = choices[random.randint(0, len(choices)-1)]
        loon_room = map.get_room_entity_moved_to(loon_room, loon_room_picked)
        
    #Nudges the loon if he gets stuck for too long
    if loon_room_prev==loon_room:
        turns_not_moving+=1
    else:
        turns_not_moving=0
    if turns_not_moving>=3:
        try:
            # why six? this is arbitrary.
            loon_room=map.rooms[int(loon_room)+6] #6 to move up/down then left/right once each
        except:
            loon_room=map.rooms[int(loon_room)-6]
        turns_not_moving=0

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

def print_debug_display():
    ttui.lines()
    print("Debug Display")
    print("Player room     : " + str(player_room))
    print("Loon room       : " + str(loon_room))
    print("Loon mood       : " + str(loon_mood))
    print("Loon choices    : " + str(choices))
    print("Turns not moving: " + str(turns_not_moving))
    print("Bats room       : " + str(bats_room))
    print("Status          : " + str(status))
    ttui.lines()

#Main loop
while True:
    # intro screen
    ttui.clear_screen()
    ttui.lines()
    print("Trapped")
    ttui.lines()
    answer = ttui.list_menu("Play?", ["Yes", "No"])
    if answer == "No":
        quit
    if answer == "Yes":
        ttui.clear_screen()
    
    # game setup
    player_room, loon_room, bats_room = place_entities_in_rooms()
    print(player_room)
    print(loon_room)
    # game loop
    while True:
        if debug==1:
            print_debug_display()
        
        ttui.show_stat_screen(player_room, turns_left)

        # tell user about how close the loon is
        if detectLoon()==0: # same room, end game
            if loon_mood==moods[0]:
                ttui.clear_screen()
                status=2
                break
            else:
                ttui.clear_screen()
                status=3
                break
        elif detectLoon()==1:
            print("He's close.")
            print("He sounds as if he's " + loon_mood + ".")
        elif detectLoon()==2:
            print("You hear the loon.")
        else:
            print(get_random_flavor_text())
        
        # bats
        if detectBats() == 0:
            print("You've awakened the bats.")
            player_room=map.get_random_room()
            bats_room=map.get_random_room()
            print("You hear rustling.")
        elif detectBats() == 1:
            print("You hear rustling.")
        
        # logic to always run
        moveRoom() # runs regardless of awakening the bats, which makes things a bit unclear
        loonMood()
        moveLoon()
        ttui.clear_screen()
        if turns_left<1:
            status=0
            break # end game
        else:
            turns_left -= 1
    ttui.clear_screen()
    game_over(status)
