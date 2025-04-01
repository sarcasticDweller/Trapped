# anything pertaining to the map and moving about it goes here. everyone moves the same

# python libraries
import math, random

rooms=[
    0,  1, 2, 3, 4,
    5, 6, 7, 8, 9,
    10, 11, 12, 13, 14,
    15, 16, 17, 18, 19,
    20, 21, 22, 23, 24
]

left_modifier = -1
right_modifier = 1
up_modifier = -math.sqrt(len(rooms))
down_modifier = math.sqrt(len(rooms))

def get_directions_entity_can_move(current_room):
    options = []
    if current_room + left_modifier >= 0:
        options.append("left")
    if current_room + right_modifier <= len(rooms):
        options.append("right")
    if current_room + up_modifier >= 0:
        options.append("up")
    if current_room + down_modifier <= len(rooms):
        options.append("down")
    return options

def get_room_entity_moved_to(current_room, option):
    new_room = current_room
    if option == "left":
        new_room += left_modifier
    if option == "right":
        new_room += right_modifier
    if option == "up":
        new_room += up_modifier
    if option == "down":
        new_room += down_modifier
    return new_room

def get_random_room():
    return random.choice(rooms)

def get_neighboring_objects_at_range(reference_room, target_room, dectection_range):
    output = None
    difference = target_room - reference_room
    distance = 0

    if difference == 0:
        return "same", distance

    # iterate through at increasing distance (multiplier)
    while distance <= dectection_range:
        distance += 1
        if difference == left_modifier * distance:
            output = "left" 
        if difference == right_modifier * distance:
            output = "right"
        if difference == up_modifier * distance:
            output = "up"
        if difference == down_modifier * distance:
            output = "down"
        if output != None:
            break
    
    return output, distance
