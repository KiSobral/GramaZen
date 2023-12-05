from random import random, randint
from node import Node

class Coordinates():
    start: Node
    end: Node
    current_node: Node | None

    def __init__(self):
        self.clear_all_field()


    def clear_all_field(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.current_node = None
        self.final_path = []
        self.check_points = []


    def clear_cut(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []


    def largest_distance(self):
        largest = 0

        for wall in self.walls:
            if wall[0] > largest:
                largest = wall[0]

            if wall[1] > largest:
                largest = wall[1]

        for point in self.check_points:
            if point[0] > largest:
                largest = point[0]

            if point[1] > largest:
                largest = point[1]

        return largest + 1


    def create_maze(self, gui):
        largest = self.largest_distance()

        if gui.grid_size > largest:
            largest = gui.grid_size

        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass


    def generate_random_blocks(self, gui):
        self.walls = []
        for _ in range(gui.grid_size*gui.grid_size):
            if random() > 0.6:
                wall = (randint(0, gui.grid_size-1),
                        randint(0, gui.grid_size-1))
                if wall not in self.walls:
                    self.walls.append(wall)
