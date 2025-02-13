import numpy as np
import networkx as nx
import random

class GraphUtil():
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self._graph = None
        self._walls = set()
        self._avg_reachability = 1

    @property
    def graph(self):
        return self._graph
    
    @property
    def walls(self):
        return self._walls
    
    @property
    def avg_reachability(self):
        self.compute_normalized_reachability()
        return self._avg_reachability
    
    @staticmethod
    def is_fully_connected(graph):
        return nx.is_connected(graph)
    
    @staticmethod
    def create_empty_graph():
        return nx.Graph()

    def set_wall_count(self, wall_count):
        self._wall_count = wall_count

    def build_graph(self):
        self._graph = nx.Graph()
        
        # Add nodes for every tile in the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self._graph.add_node((x, y))
        
        # Add edges for adjacent tiles (no walls initially)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if x < self.grid_size - 1:  # Horizontal edge
                    self._graph.add_edge((x, y), (x + 1, y))
                if y < self.grid_size - 1:  # Vertical edge
                    self._graph.add_edge((x, y), (x, y + 1))
    
    def place_wall_and_check_connectivity(self, wall): 
        # Add the wall by removing the corresponding edge in the graph
        self._graph.remove_edge(wall[0], wall[1])
        
        # Check if the grid is still fully connected
        if not GraphUtil.is_fully_connected(self._graph):
            # If the grid is disconnected, remove the wall (restore the edge)
            self._graph.add_edge(wall[0], wall[1])
        else:
            # The grid is still fully connected, add the wall to the set
            self._walls.add(wall)
            return True
        return False
    
    def place_walls(self, wall_candidates):
        placed_walls = 0
        while placed_walls < self._wall_count and wall_candidates:
            wall = wall_candidates.pop()
            if self.place_wall_and_check_connectivity(wall):
                placed_walls += 1
        return placed_walls

    def place_random_walls(self):
        wall_candidates = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if x < self.grid_size - 1:
                    wall_candidates.append(((x, y), (x + 1, y)))  # Horizontal wall
                if y < self.grid_size - 1:
                    wall_candidates.append(((x, y), (x, y + 1)))  # Vertical wall
        random.shuffle(wall_candidates)
        return self.place_walls(wall_candidates)
    
    def place_fixed_walls(self, wall_candidates):
        return self.place_walls(list(wall_candidates))

    def max_degree(self, pos):
        """Define max degree per tile in an unwalled grid"""
        x, y = pos
        if (x in [0, self.grid_size-1] and y in [0, self.grid_size-1]):  # Corner tiles
            return 2
        elif x in [0, self.grid_size-1] or y in [0, self.grid_size-1]:   # Edge tiles (not corners)
            return 3
        else:  # Interior tiles
            return 4
    
    def compute_normalized_reachability(self):
        """
        Calculates the degree of each node against its theoretical max.
        Takes the average of this calculation on all nodes
        """
        reachability_values = []
        for node in self._graph.nodes:
            d_current = self._graph.degree(node)   # Current degree
            d_max = self.max_degree(node)     # Unwalled max degree
            reachability = d_current / d_max  # Normalized reachability
            reachability_values.append(reachability)
        self._avg_reachability = np.mean(reachability_values)
        return
    
    def find_shortest_path(self, source, target):
        shortest_path = nx.shortest_path(self._graph, source=source, target=target)
        return shortest_path

    def find_long_branches(self):
        """
        Find long branches in the network.
        Branches are defined as starting from degree-1 nodes, traversing a chain of 1+ degree-2 nodes
        until a node of degree greater than 2 is reached.
        """
        branches = []
        visited = set()

        # Identify degree-1 nodes (starting points)
        start_nodes = [node for node in self._graph.nodes if self._graph.degree(node) == 1]

        for start in start_nodes:
            if start in visited:
                continue
            
            branch = [start]
            current = start
            visited.add(current)

            # Follow the chain of degree-2 nodes
            while True:
                neighbors = [n for n in self._graph.neighbors(current) if n not in visited]
                if len(neighbors) != 1:  # Stop if no valid path forward or reached a higher-degree node
                    break

                next_node = neighbors[0]
                if self._graph.degree(next_node) != 2:  # Stop at the first node with degree >2
                    break
                
                branch.append(next_node)
                visited.add(next_node)
                current = next_node

            if len(branch) > 1:  # Only count meaningful branches
                branches.append(branch)

        return branches

    def plot_network(self):
        import matplotlib.pyplot as plt

        branches = self.find_long_branches()
    
        plt.figure(figsize=(5,5))

        pos = {node: (node[0], node[1]) for node in self._graph.nodes()}  # Flip y-coordinates for visualization
        nx.draw(self._graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=12)
        # nx.draw(self._graph, with_labels=True)

        # Highlight branches
        for branch in branches:
            nx.draw_networkx_nodes(self._graph, pos, nodelist=branch, node_color='red', node_size=700)

        plt.show()

