from burglebros.utilities.graph_utils import GraphUtil

class WallGenerator():
    def __init__(self, graph_util):
        self.gu = graph_util

    def get_random_wall_placement(self):
        self.gu.place_random_walls()
        return self.gu.walls
    
    def get_fixed_wall_placement(self, floor_number):
        walls= set()
        if floor_number == 0:
            walls.add(((0,0),(1,0)))
            walls.add(((1,0),(2,0)))
            walls.add(((3,0),(3,1)))
            walls.add(((0,1),(0,2)))
            walls.add(((1,1),(1,2)))
            walls.add(((2,2),(3,2)))
            walls.add(((2,2),(2,3)))
            walls.add(((0,3),(1,3)))
        else:
            pass
            # TODO: Handle other floors
        self.gu.place_fixed_walls(walls)
        return self.gu.walls

if __name__ == "__main__":
    gu = GraphUtil(4)
    gu.set_wall_count(8)
    gu.build_graph()
    rwg = WallGenerator(gu)
    rwg.get_random_wall_placement()
    print(gu.compute_normalized_reachability())
    gu.plot_network()
