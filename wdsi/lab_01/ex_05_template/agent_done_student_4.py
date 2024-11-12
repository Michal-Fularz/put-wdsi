# prob.py
# This is

import random
import numpy as np
import queue
import math
from queue import PriorityQueue

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
        action = 'N'

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE
        action = self.actions[self.t]
        self.t += 1

        # ------------------

        return action

    def find_path(self):
        path = []
        actions = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE
        s = self.loc
        g = self.goal
        d = self.dir
        visited = set()
        cost = {(location, orientation): math.inf for location in self.locations for orientation in ['N', 'E', 'S', 'W']}
        parent = {(location, orientation): None for location in self.locations for orientation in ['N', 'E', 'S', 'W']}
        q = PriorityQueue()
        q.put((0, (s, d)))
        cost[(s, d)] = 0

        while not q.empty():
            cur_cost, (cur_location, cur_direction) = q.get()
            if (cur_location, cur_direction) in visited:
                continue
            visited.add((cur_location, cur_direction))

            if cur_location == g:
                break

            for (new_location, new_direction, action, move_cost) in self.get_neighbors(cur_location, cur_direction):
                if (new_location, new_direction) in visited:
                    continue

                new_cost = cur_cost + move_cost
                if new_cost < cost[(new_location, new_direction)]:
                    cost[(new_location, new_direction)] = new_cost
                    parent[(new_location, new_direction)] = ((cur_location, cur_direction), action)
                    priority = new_cost + self.heuristic(new_location, g)
                    q.put((priority, (new_location, new_direction)))

        cur_node = min(((g, d) for d in ['N', 'E', 'S', 'W']), key=lambda x: cost[x])
        while cur_node is not None and parent[cur_node] is not None:
            path.append(cur_node[0])
            cur_node, action = parent[cur_node]
            actions.append(action)

        path.reverse()
        actions.reverse()
        
        # ------------------

        return path, actions

    def get_neighbors(self, location, orientation):
        neighbors = []
        x, y = location
        forward_moves = {
            'N': (x, y + 1),
            'S': (x, y - 1),
            'E': (x + 1, y),
            'W': (x - 1, y)
        }

        if forward_moves[orientation] in self.locations:
            neighbors.append((forward_moves[orientation], orientation, 'forward', 1)) 

        new_orientation = self.turn_left(orientation)
        neighbors.append((location, new_orientation, 'turnleft', 5))

        new_orientation = self.turn_right(orientation)
        neighbors.append((location, new_orientation, 'turnright', 2))

        return neighbors
    
    def turn_right(self, orientation):
        directions = ['N', 'E', 'S', 'W']
        idx = directions.index(orientation)
        return directions[(idx + 1) % 4]
    
    def turn_left(self, orientation):
        directions = ['N', 'W', 'S', 'E']
        idx = directions.index(orientation)
        return directions[(idx + 1) % 4]
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_path(self):
        return self.path