import random
import networkx as nx

class RandomWallGenerator():
    def __init__(self, grid_size, wall_count):
        self.grid_size = grid_size
        self.wall_count = wall_count

    def get_random_wall_placement(self):
        self.create_grid()
        self.place_walls()
        return self.walls
        
    def create_grid(self):
        return [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def get_neighbors(self, x, y):
        neighbors = []
        if x > 0: 
            neighbors.append((x - 1, y))
        if y > 0: 
            neighbors.append((x, y - 1))
        if x < self.grid_size - 1: 
            neighbors.append((x + 1, y))
        if y < self.grid_size - 1: 
            neighbors.append((x, y + 1))
        return neighbors

    @staticmethod
    def is_fully_connected(graph):
        # Check if the grid is fully connected
        return nx.is_connected(graph)

    def place_walls(self):
        G = nx.Graph()  # Create the graph
        
        # Add nodes for every tile in the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                G.add_node((x, y))
        
        # Add edges for adjacent tiles (no walls initially)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if x < self.grid_size - 1:  # Horizontal edge
                    G.add_edge((x, y), (x + 1, y))
                if y < self.grid_size - 1:  # Vertical edge
                    G.add_edge((x, y), (x, y + 1))
        
        wall_candidates = []
        
        # Prepare list of possible wall placements
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if x < self.grid_size - 1:
                    wall_candidates.append(((x, y), (x + 1, y)))  # Horizontal wall
                if y < self.grid_size - 1:
                    wall_candidates.append(((x, y), (x, y + 1)))  # Vertical wall
        
        random.shuffle(wall_candidates)
        
        self.walls = set()
        placed_walls = 0
        
        # Place walls and check connectivity
        while placed_walls < self.wall_count and wall_candidates:
            wall = wall_candidates.pop()
            self.walls.add(wall)
            
            # Add the wall by removing the corresponding edge in the graph
            G.remove_edge(wall[0], wall[1])
            
            # Check if the grid is still fully connected
            if not RandomWallGenerator.is_fully_connected(G):
                # If the grid is disconnected, remove the wall (restore the edge)
                G.add_edge(wall[0], wall[1])
                self.walls.remove(wall)
            else:
                placed_walls += 1
        
        return

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


if __name__ == "__main__":
    rwg = RandomWallGenerator(grid_size=4, wall_count=8)
    rwg.create_grid()
    rwg.place_walls()
    rwg.print_grid()
