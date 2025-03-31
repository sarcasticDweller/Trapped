import random, os, math

#List library
rooms=[
0,  1, 2, 3, 4,
5, 6, 7, 8, 9,
10, 11, 12, 13, 14,
15, 16, 17, 18, 19,
20, 21, 22, 23, 24
]
"""Rooms grid for ease of access:
    24 23 22 21 20
    19 18 17 16 15
    14 13 12 11 10
    9  8  7  6  5
    4  3  2  1  0"""
#Note: moods[0] MUST be a volatile mood.
#Note: moods[2] MUST be a passive mood.
moods=["cranky", "mellow", "asleep"]
choices=[]
#Room declarations
player_room=rooms[math.floor((len(rooms)-1)/2)] # should always be 12
while True:
    loon_room=rooms[random.randint(0, len(rooms)-1)]
    if loon_room!=player_room:
        break
bats_room=rooms[random.randint(0, len(rooms)-1)]
loon_room_prev=loon_room
turns_not_moving=0
loon_mood=moods[random.randint(0, len(moods)-1)]
#Variable declarations
turns_left=50 #Default is 50
debug=0 #1 for debug
answer="12"
up=""
down=""
left=""
right=""
na="na"
"""Status meanings:
    0= Time out
    1= Dead to non-loon-entity
    2= Dead to loon
    3= Victory
    4= Game playing"""
status=4
#Function declarations
def lines():
    print("//////////////////////////////////")
def moveRoom():
    #Moves the player since it doesn't work well in the main loop
    global player_room #Prevents an error. :/
    #Because borders freak Python out this is here.

    # this is deceptively clever. the player space is a linear list, but this gives the player agency to jump to points along the list. i love this concept, but it could be made more modular. this only works in a 5^2 list.
    try:
        up=str(rooms[player_room+5])
    except:
        up=na
    try:
        down=str(rooms[player_room-5])
    except:
        down=na
    try:
        left=str(rooms[player_room-1])
    except:
        left=na
    try:
        right=str(rooms[player_room+1])
    except:
        right=na
    print("You can do these actions:")
    print("Go up   : " + up)
    print("Go down : " + down)
    print("Go left : " + left)
    print("Go right: " + right)
    print("Or wait : [.]")
    while True:
        answer=input(":: ")
        if answer==up or answer==down or answer==left or answer==right:
            if answer!=na:
                player_room=rooms[int(answer)]
                break
            else:
                print("You feel the soft cushioning on the wall. There\nare gash marks in one of the cushions.")
                print("Alas, you must pick a different direction.")
        elif answer==".":
            player_room=player_room
            break
        else:
            print("That's not a valid answer.")
def clear_screen():
    # clears the screen
    try:
        # assuming we're running a linux/mac
        os.system("clear")
    except:
        # we must be on windows
        os.system("cls")

def ui():
    #Presents the user with their stats.
    global turns_left # this should be a parameter, not a global variable declared in a function
    turns_left-=1
    lines()
    print("Room      : " + str(player_room))
    print("Turns left: " + str(turns_left))
    lines()
def detectLoon():
    """Return value meanings:
        0=not near
        1=next to
        2=two away
        3=in loon room"""
    global status
    if player_room==int(loon_room):
        return 3
    if player_room==int(loon_room)-1:
        return 1
    elif player_room==int(loon_room)+1:
        return 1
    elif player_room==int(loon_room)+5:
        return 1
    elif player_room==int(loon_room)-5:
        return 1
    elif player_room==int(loon_room)-2:
        return 2
    elif player_room==int(loon_room)+2:
        return 2
    elif player_room==int(loon_room)-10:
        return 2
    elif player_room==int(loon_room)+10:
        return 2
    else:
        return 0
def detectBats():
    """Return value meanings:
        0=not near
        1=next to
        2=in bats room"""
    global status
    if player_room==int(bats_room):
        return 2
    if player_room==int(bats_room)-1:
        return 1
    elif player_room==int(bats_room)+1:
        return 1
    elif player_room==int(bats_room)+5:
        return 1
    elif player_room==int(bats_room)-5:
        return 1
    else:
        return 0
def get_random_flavor_text():
    statements=["You know he's here somewhere...",
                "He's not in this room.", 
                "I will find him soon.",
                "If I give up now I'll never escape."
    ]
    return statements[random.randint(0, len(statements)-1)]
def loonMood():
    #Handles the randomization of the loon's mood.
    global loon_mood
    if turns_left%2==0:
        loon_mood=moods[random.randint(0, len(moods)-1)]
def moveLoon(): #Broken. Loon went from 0-20 then it broke when I tried to go to 0 to attempt that.
    global loon_room
    global loon_room_prev
    global choices
    global turns_not_moving
    choices=[]
    loon_room_prev=loon_room
    if loon_mood!=moods[2]:
        #Generates choices
        try:
            choices.append(str(rooms[loon_room+5]))
        except:
            choices.append(na)
        try:
            choices.append(str(rooms[loon_room-5]))
        except:
            choices.append(na)
        try:
            choices.append(str(rooms[loon_room-1]))
        except:
            choices.append(na)
        try:
            choices.append(str(rooms[loon_room+1]))
        except:
            choices.append(na)
        for i in range(choices.count(na)):
            choices.remove(na)
        #Loon picks a room
        try:
            loon_room=choices[random.randint(0, len(choices)-1)]
        except:
            loon_room=loon_room
    #Nudges the loon if he gets stuck for too long
    if loon_room_prev==loon_room:
        turns_not_moving+=1
    else:
        turns_not_moving=0
    if turns_not_moving>=3:
        try:
            loon_room=rooms[int(loon_room)+6] #6 to move up/down then left/right once each
        except:
            loon_room=rooms[int(loon_room)-6]
        turns_not_mocing=0
def game_over(status):
    #Prints game-over messages

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

def pause():
    pause=input("Press enter to continue...")

def print_debug_display():
    lines()
    print("Debug Display")
    print("Player room     : " + str(player_room))
    print("Loon room       : " + str(loon_room))
    print("Loon mood       : " + str(loon_mood))
    print("Loon choices    : " + str(choices))
    print("Turns not moving: " + str(turns_not_moving))
    print("Bats room       : " + str(bats_room))
    print("Status          : " + str(status))
    lines()

#Main loop
while True:
    clear_screen()
    lines()
    print("Trapped")
    lines()
    answer=input("Play?\nYes: 1\nNo : 2\n(Enter one)\n:: ")
    if answer=="1":
        clear_screen()
        clear_screen()
        while True:
            if debug==1:
                print_debug_display()
            ui()
            if detectLoon()==0:
                print(get_random_flavor_text())
            elif detectLoon()==1:
                print("He's close.")
                print("He sounds as if he's " + loon_mood + ".")
            elif detectLoon()==2:
                print("You hear the loon.")
            elif detectLoon()==3:
                if loon_mood==moods[0]:
                    clear_screen()
                    status=2
                    break
                else:
                    clear_screen()
                    status=3
            if detectBats()==1:
                print("You hear rustling.")
            elif detectBats()==2:
                print("You've awakened the bats.")
                player_room=rooms[random.randint(0, len(rooms)-1)]
                bats_room=rooms[random.randint(0, len(rooms)-1)]
            moveRoom()
            loonMood()
            moveLoon()
            clear_screen()
            if turns_left<1:
                status=0
                break
        clear_screen()
        game_over(status)
    elif answer=="2":
        break
    else:
        print("Invalid.")
        pause()
