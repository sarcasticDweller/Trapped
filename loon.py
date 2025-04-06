# python libraries
import random
# project libraries
import map

class Loon:
    def __init__(self, room):
        self.moods = ["cranky", "mellow", "asleep"]
        self.mood = self.set_mood()
        """
        cranky: lethal & mobile
        mellow: passive & mobile
        asleep: passive & immobile
        """
        self.room = room
        self.room_previous = self.room
        self.__turns_not_moving = 0
        self.__turns_not_moving_max = 3
        self.rooms_visited = [self.room] # add each room it visits to this, and then let the player know when they've been to a room visited
    def set_mood(self):
        # note: original code set this to go whenever the turns left was even. should create logic to do this every other turn
        self.mood = random.choice(self.moods)

    def move_room(self):
        self.room_previous = self.room
        choices = map.get_directions_entity_can_move(self.room)
        room_picked = random.choice(choices)
        self.room = map.get_room_entity_moved_to(self.room, room_picked)
        self.rooms_visited.append(self.room)
        self.__turns_not_moving = 0

    def nudge_if_sleeping_too_long(self):
        if self.__turns_not_moving >= self.__turns_not_moving_max:
            self.move_room()
    
    def update(self):
        self.set_mood()
        if self.mood != "asleep":
            self.move_room()
        self.nudge_if_sleeping_too_long()
        
