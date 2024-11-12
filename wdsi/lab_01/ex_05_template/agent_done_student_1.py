

import random
from cmath import acosh

import numpy as np
import queue
import math

from gridutil import generate_locations


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
        self.path, self.actions = self.find_path()

    def __call__(self):
        action = self.actions.pop(0)
        return action

    @staticmethod
    def heuristic(cel, neighbor, cur):
        ((n_x, n_y), n_or) = neighbor
        ((c_x, c_y), c_or) = cur

        action_cost = 0

        if c_or == n_or:
            action_cost = 1
        elif c_or == "N" and n_or == "W" or c_or == "E" and n_or == "N" or \
                c_or == "S" and n_or == "E" or c_or == "W" and n_or == "S":
            action_cost = 5
        elif c_or == "N" and n_or == "E" or c_or == "E" and n_or == "S" or \
                c_or == "S" and n_or == "W" or c_or == "W" and n_or == "N":
            action_cost = 2

        return action_cost

    @staticmethod
    def get_neighbors(loc, size, walls):
        neighbors = []

        (x, y), orientation = loc
        new_x, new_y = 0, 0

        if orientation == "N":
            new_x, new_y = x, y + 1
        elif orientation == "E":
            new_x, new_y = x + 1, y
        elif orientation == "S":
            new_x, new_y = x, y - 1
        elif orientation == "W":
            new_x, new_y = x - 1, y

        if 0 <= new_x < size and 0 <= new_y < size and (new_x, new_y) not in walls:
            neighbors.append(((new_x, new_y), orientation))

        left_orientation = ''
        right_orientation = ''

        if orientation == "N":
            left_orientation = "W"
        elif orientation == "E":
            left_orientation = "N"
        elif orientation == "S":
            left_orientation = "E"
        elif orientation == "W":
            left_orientation = "S"
        neighbors.append(((x, y), left_orientation))

        if orientation == "N":
            right_orientation = "E"
        elif orientation == "E":
            right_orientation = "S"
        elif orientation == "S":
            right_orientation = "W"
        elif orientation == "W":
            right_orientation = "N"
        neighbors.append(((x, y), right_orientation))

        return neighbors

    def find_path(self):
        orientations = ['N', 'E', 'W', 'S']

        all_states = [((x, y), orientation) for (x, y) in self.locations for orientation in orientations]

        s = (self.loc, self.dir)
        g = (self.goal, self.dir)

        visited = set()
        cost = {n: math.inf for n in all_states}
        parent = {n: None for n in all_states}
        q = queue.PriorityQueue()

        cost[s] = 0
        q.put((0, s))

        while not q.empty():
            _, cur_n = q.get()

            if cur_n in visited:
                continue

            visited.add(cur_n)

            if cur_n == g:
                break

            for nh in self.get_neighbors(cur_n, self.size, self.walls):
                if nh in visited:
                    continue

                new_cost = cost[cur_n] + 1

                if new_cost < cost[nh]:
                    cost[nh] = new_cost
                    parent[nh] = cur_n

                    priority = new_cost + self.heuristic(g, nh, cur_n)
                    q.put((priority, nh))

        actions = []
        path_w_or = []
        cur_n = g
        while cur_n is not None:
            path_w_or.append(cur_n)
            cur_n = parent[cur_n]

        path_w_or.reverse()

        path = [(x, y) for (x, y), _ in path_w_or]

        orientations = {'N': 0, 'E': 1, 'S': 2, 'W': 3}

        for i in range(len(path_w_or) - 1):
            ((x1, y1), or1) = path_w_or[i]
            ((x2, y2), or2) = path_w_or[i + 1]

            if or1 == or2:
                if x1 != x2 or y1 != y2:
                    actions.append("forward")
            else:
                if (or1 == "N" and or2 == "W") or (or1 == "E" and or2 == "N") or \
                        (or1 == "S" and or2 == "E") or (or1 == "W" and or2 == "S"):
                    actions.append("turnleft")
                elif (or1 == "N" and or2 == "E") or (or1 == "E" and or2 == "S") or \
                        (or1 == "S" and or2 == "W") or (or1 == "W" and or2 == "N"):
                    actions.append("turnright")

        print(parent)
        print(path_w_or)
        print(actions)
        return path, actions

    def get_path(self):
        return self.path
