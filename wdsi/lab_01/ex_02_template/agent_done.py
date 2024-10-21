import random
import queue

import numpy as np

from gridutil import generate_locations
from wdsi.lab_01.lab_01_ex_01 import bfs


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path = self.find_path()

    def __call__(self):
        action = 'N'

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE



        # ------------------

        return action

    def find_path(self):
        path = []

        # find path from self.loc to self.goal
        # TODO PUT YOUR CODE HERE
        graph = self.generate_graph_for_bfs()
        path_idx = bfs(
            self.loc_to_idx[self.loc],
            self.loc_to_idx[self.goal],
            graph
        )
        idx_to_loc = {idx: loc for idx, loc in enumerate(self.locations)}
        for e in path_idx:
            path.append(idx_to_loc[e])

        # ------------------

        return path

    def get_path(self):
        return self.path

    def generate_graph_for_bfs(self) -> dict[int, list[int]]:
        graph_locations = create_adjacency_list(self.locations)

        graph = {}
        for key, value in graph_locations.items():
            adjacent_vertices = []
            for v in value:
                adjacent_vertices.append(self.loc_to_idx[v])
            graph[self.loc_to_idx[key]] = adjacent_vertices

        return graph


def create_adjacency_list(coords: list[(int, int)]) -> dict[(int, int), list[(int, int)]]:
    adjacency_list = {}

    # Iterate over each pair of coordinates
    for coord in coords:
        adjacency_list[coord] = []  # Initialize empty list for each coordinate

        for other_coord in coords:
            if coord != other_coord:
                # Check if the coordinates differ by 1 in x or y, but not both
                if (abs(coord[0] - other_coord[0]) == 1 and coord[1] == other_coord[1]) or \
                        (abs(coord[1] - other_coord[1]) == 1 and coord[0] == other_coord[0]):
                    adjacency_list[coord].append(other_coord)

    return adjacency_list
