"""
"""

import random
from burglebros.modules.guard import Guard
from burglebros.utilities.wall_generation import WallGenerator
from burglebros.utilities.graph_utils import GraphUtil
from burglebros.configs.configs import *
from burglebros.utilities.vprint import vprint

class Floor:
    def __init__(self, grid_size=4, wall_count=8, floor_number=0):
        self.grid_size = grid_size
        self.wall_count = wall_count
        self.number = floor_number
        self.safe_cracked = False
        self.safe_location_discovered = False
        self.grid = [['Empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid_all_coordinates = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        self.guard = Guard(self.grid_all_coordinates, starting_speed=self.number+2, guard_number=self.number, grid_size=self.grid_size)
        self.walls = set()

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

        # Create a graph representation of the grid
        self.gu = GraphUtil(self.grid_size)
        self.gu.build_graph()

        # Add walls
        if USE_WALLS:
            self.wall_gen = WallGenerator(self.gu)
            self.gu.set_wall_count(self.wall_count)
            if FIXED_WALLS:
                self.walls = self.wall_gen.get_fixed_wall_placement(self.number)
            else:
                self.walls = self.wall_gen.get_random_wall_placement()
        self.guard.add_wall_info(self.walls)
        self.guard.add_graph_util(self.gu)
        vprint(f"Floor {self.number} walls set: {self.walls}")

    def print_grid(self):
        print("\n")
        for y in range(self.grid_size - 1, -1, -1):  # Start printing from top to bottom (y-axis)
            # Print tiles with vertical walls
            row_tiles = ""
            for x in range(self.grid_size):
                row_tiles += f"({x},{y})"
                if ((x, y), (x + 1, y)) in self.walls or ((x + 1, y), (x, y)) in self.walls:
                    row_tiles += "|"
                else:
                    row_tiles += " "
            print(row_tiles)
            
            # Print horizontal walls if not at the bottom row
            if y > 0:
                row_walls = ""
                for x in range(self.grid_size):
                    if ((x, y - 1), (x, y)) in self.walls or ((x, y), (x, y - 1)) in self.walls:
                        row_walls += "-----"
                    else:
                        row_walls += "      "
                print(row_walls)