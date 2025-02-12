"""
"""

import random
from collections import deque
from burglebros.utilities.vprint import vprint

class Guard:

    # Define movement directions in clockwise order: Right → Down → Left → Up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, grid_size, grid_all_coordinates, starting_speed):
        self.grid_size = grid_size
        self.grid_all_coordinates = grid_all_coordinates
        self.speed = starting_speed

        self.x, self.y = grid_size - 1, grid_size - 1  # Start at top-right
        self.patrol_route = self.grid_all_coordinates.copy()
        random.shuffle(self.patrol_route)
        self.patrol_route_index = 0
        self.current_target = self.patrol_route[self.patrol_route_index]
        self.current_path = self.find_path((self.x, self.y), self.current_target)

    def find_path(self, start, end):
        """Finds the shortest path from start to end using BFS with clockwise priority."""
        
        def is_valid(x, y, grid_size):
            """Check if the coordinate is within grid bounds."""
            return 0 <= x < grid_size and 0 <= y < grid_size
    
        queue = deque([(start, [])])  # Queue stores (current_position, path_taken)
        visited = set()
        visited.add(start)

        while queue:
            (x, y), path = queue.popleft()

            # If reached destination, return the path
            if (x, y) == end:
                return path + [(x, y)]

            for dx, dy in self.directions:  # Prioritizing clockwise movement
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, self.grid_size) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(x, y)]))
                    visited.add((nx, ny))

        return []  # No path found (shouldn't happen in an open grid)

    def take_turn(self):
        """Moves the guard."""
        if self.current_path:
            next_pos = self.current_path.pop()
            self.x, self.y = next_pos
            if next_pos == self.current_target:
                self.get_new_target()
        else:
            vprint(f"Does this happen?")
            self.get_new_target()
    
    def do_all_guard_movement(self):
        for _ in range(self.speed-1):
            self.move()

    def get_new_target(self):

        while ((self.x, self.y) == self.current_target):

            # Technically we should remove the current location first and then shuffle the remainder, but I'm lazy
            if self.patrol_route_index == len(self.patrol_route)-1:
                random.shuffle(self.patrol_route)
                self.patrol_route_index = 0
            else:
                self.patrol_route_index += 1
            self.current_target = self.patrol_route[self.patrol_route_index]
            self.current_path = self.find_path((self.x, self.y), self.current_target)

    def add_alarm(self, x, y):
        pass
        # vprint("TODO. Change target, increase speed")