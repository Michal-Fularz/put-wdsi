import random
import numpy as np
import queue

from gridutil import generate_locations


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        print(self.locations)
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path = self.find_path()

    def __call__(self):
        next_loc = self.path[1]
        dx, dy = next_loc
        x, y = self.loc

        print(self.path)
        print(dx, dy)
        print(x, y)
        action = ''

        if dx - x == 1:
            action = 'E'
        elif dx - x == -1:
            action = 'W'
        elif dy - y == -1:
            action = 'S'
        elif dy - y == 1:
            action = 'N'

        # ------------------
        self.path.pop(0)
        self.loc = next_loc
        return action

    @staticmethod
    def get_neighbors(loc, size, walls):
        neighbors = []
        x, y = loc
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in possible_moves:
            new_loc = (x + dx, y + dy)
            if 0 <= new_loc[0] < size and 0 <= new_loc[1] < size and new_loc not in walls:
                neighbors.append(new_loc)

        return neighbors

    def find_path(self):
        parent = {self.loc: None}
        q = queue.Queue()
        q.put(self.loc)

        while not q.empty():
            cur_loc = q.get()

            if cur_loc == self.goal:
                break

            for neighbor in self.get_neighbors(cur_loc, self.size, self.walls):
                if neighbor not in parent:
                    parent[neighbor] = cur_loc
                    q.put(neighbor)

        path = []
        cur_loc = self.goal
        while cur_loc is not None:
            path.append(cur_loc)
            cur_loc = parent[cur_loc]

        path.reverse()
        return path

    def get_path(self):
        return self.path
