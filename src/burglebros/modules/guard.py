"""
TODO: Add alarm handling
"""

import random
from collections import deque
from burglebros.utilities.vprint import vprint

class Guard:

    # Define movement directions in clockwise order: Right → Down → Left → Up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, grid_all_coordinates, starting_speed, guard_number=0, grid_size=3):
        self.grid_all_coordinates = grid_all_coordinates
        self.speed = starting_speed
        self.number = guard_number
        self.grid_size = grid_size

        self.x, self.y = grid_size - 1, grid_size - 1  # Start at top-right
        self.patrol_route = self.grid_all_coordinates.copy()
        random.shuffle(self.patrol_route)
        self.patrol_route_index = 0
        self.current_target = self.patrol_route[self.patrol_route_index]
        self.current_path = []

    def add_wall_info(self, walls):
        self.walls = walls

    def add_graph_util(self, graph_util):
        self.gu = graph_util

    def find_shortest_path(self, start, end):
        """
        NOTE: This does not guarantee it will follow a clockwise path!
        """
        path = self.gu.find_shortest_path(start, end)
        return path

    def take_turn(self):
        """Moves the guard."""
        vprint(f"Guard on floor {self.number} taking his turn.")
        self.do_all_guard_movement()
    
    def is_move_valid(self, dx, dy):
        """Ensure an attempted move would be valid (within boundaries)."""
        is_valid = False
        new_x, new_y = self.x + dx, self.y + dy

        self.can_move_up = ((self.x, self.y), (self.x, self.y + 1)) not in self.walls and ((self.x, self.y + 1), (self.x, self.y)) not in self.walls
        self.can_move_down = ((self.x, self.y), (self.x, self.y - 1)) not in self.walls and ((self.x, self.y - 1), (self.x, self.y)) not in self.walls
        self.can_move_left = ((self.x, self.y), (self.x - 1, self.y)) not in self.walls and ((self.x - 1, self.y), (self.x, self.y)) not in self.walls
        self.can_move_right = ((self.x, self.y), (self.x + 1, self.y)) not in self.walls and ((self.x + 1, self.y), (self.x, self.y)) not in self.walls

        # Ensure the agent doesn't move off the grid
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            # Ensure the agent doesn't move through a wall
            if dx == 0 and dy == 1:
                if self.can_move_up:
                    is_valid = True
            elif dx == 0 and dy == -1:
                if self.can_move_down:
                    is_valid = True
            elif dx == 1 and dy == 0:
                if self.can_move_right:
                    is_valid = True
            elif dx == -1 and dy == 0:
                if self.can_move_left:
                    is_valid = True

        return is_valid

    def move(self, next_pos):
        """Moves the guard"""
        self.x, self.y = next_pos

    def do_all_guard_movement(self):
        for _ in range(self.speed-1):
            if not self.current_path:
                vprint(f"Guard on floor {self.number} acquiring new target")
                self.get_new_target()

            next_pos = self.current_path.pop(0)
            self.move(next_pos)
            if (self.x, self.y) == self.current_target:
                vprint(f"Guard on floor {self.number} acquiring new target")
                self.get_new_target()

    def get_new_target(self):
        while ((self.x, self.y) == self.current_target):

            # Technically we should remove the current location first and then shuffle the remainder, but I'm lazy
            if self.patrol_route_index == len(self.patrol_route)-1:
                random.shuffle(self.patrol_route)
                self.patrol_route_index = 0
            else:
                self.patrol_route_index += 1
            self.current_target = self.patrol_route[self.patrol_route_index]
        self.current_path = self.find_shortest_path((self.x, self.y), self.current_target)
        vprint(f"Guard on floor {self.number} following path: {self.current_path}")

    def add_alarm(self, x, y):
        pass
        # vprint("TODO. Change target, increase speed")