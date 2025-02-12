"""
"""

import random
from burglebros.modules.guard import Guard
from burglebros.utilities.random_wall_generation import RandomWallGenerator
from burglebros.utilities.vprint import vprint

class Floor:
    def __init__(self, grid_size=4, wall_count=8, number=0):
        self.grid_size = grid_size
        self.wall_count = wall_count
        self.number = number # Bottom floor is 0, then it increases
        self.safe_cracked = False
        self.safe_location_discovered = False
        self.grid = [['Empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid_all_coordinates = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        self.guard = Guard(self.grid_size, self.grid_all_coordinates, 2)
        self.rwg = RandomWallGenerator(self.grid_size, self.wall_count)

    def add_random_walls(self):
        self.walls = self.rwg.get_random_wall_placement()
        vprint(f"Floor {self.number} walls set: {self.walls}")

    def generate_random_layout(self):
        # Randomly place the safe somewhere not on the starting tile
        safe_x, safe_y = random.randint(0, 3), random.randint(0, 3)
        while safe_x==0 and safe_y==0:
            safe_x, safe_y = random.randint(0, 3), random.randint(0, 3)
        self.grid[safe_x][safe_y] = 'Safe'
        self.safe_location = safe_x, safe_y
        vprint(f"FLOOR {self.number} SAFE LOCATION = {safe_x},{safe_y}")

        # Randomly place the stairs somewhere that's not the safe or the starting tile
        stairs_x, stairs_y = random.randint(0, 3), random.randint(0, 3)
        while (stairs_x==safe_x and stairs_y==safe_y) or (stairs_x==0 and stairs_y==0):
            stairs_x, stairs_y = random.randint(0, 3), random.randint(0, 3)
        self.grid[stairs_x][stairs_y] = 'Stairs'
        self.stairs_location = stairs_x, stairs_y
        vprint(f"FLOOR {self.number} STAIRS LOCATION = {stairs_x},{stairs_y}")

        # Randomly place traps
        for _ in range(3):
            x, y = random.randint(0, 3), random.randint(0, 3)
            if self.grid[x][y] == 'Empty':
                self.grid[x][y] = random.choice(['Normal', 'Trap'])

        # Add walls
        # TODO: When ready, uncomment this
        # self.add_random_walls()