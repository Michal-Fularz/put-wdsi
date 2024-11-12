import random
import numpy as np
import queue
from gridutil import *

class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # List of valid locations
        self.locations = list({*generate_locations(self.size)}.difference(self.walls))
        # Dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir 
        self.goal = goal

        self.t = 0
        self.path, self.actions = self.find_path()
        self.action_index = 0 

    def __call__(self):
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            self.action_index += 1
            return action
        return 'N' 

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        path = []
        actions = []

        visited = set()
        cost = { (loc, ori): float('inf') for loc in self.locations for ori in ['N', 'E', 'S', 'W'] }
        parent = { (loc, ori): None for loc in self.locations for ori in ['N', 'E', 'S', 'W'] }
        q = queue.PriorityQueue()

        q.put((0, (self.loc, self.dir)))
        cost[(self.loc, self.dir)] = 0

        while not q.empty():
            _, (cur_loc, cur_dir) = q.get()

            if (cur_loc, cur_dir) in visited:
                continue
            visited.add((cur_loc, cur_dir))

            if cur_loc == self.goal:
                break

            for (new_loc, new_dir, action, move_cost) in self.get_neighbors(cur_loc, cur_dir):
                if (new_loc, new_dir) in visited:
                    continue

                old_cost = cost[(new_loc, new_dir)]
                new_cost = cost[(cur_loc, cur_dir)] + move_cost

                if new_cost < old_cost:
                    cost[(new_loc, new_dir)] = new_cost
                    parent[(new_loc, new_dir)] = ((cur_loc, cur_dir), action)
                    priority = new_cost + self.heuristic(new_loc, self.goal)
                    q.put((priority, (new_loc, new_dir)))

        cur_node = (self.goal, cur_dir)
        while cur_node is not None and cur_node in parent:
            path.append(cur_node[0]) 
            if parent[cur_node] is not None:
                cur_node, action = parent[cur_node]
                actions.append(action)
            else:
                cur_node = None

        path.reverse() 
        actions.reverse()
        return path, actions

    def get_neighbors(self, loc, orientation):
        neighbors = []
        x, y = loc
        forward_moves = {
            'N': (x, y + 1),
            'S': (x, y - 1),
            'E': (x + 1, y),
            'W': (x - 1, y)
        }

        if forward_moves[orientation] in self.locations:
            neighbors.append((forward_moves[orientation], orientation, 'forward', 1)) 

        new_orientation = self.turn_left(orientation)
        neighbors.append((loc, new_orientation, 'turnleft', 5))

        new_orientation = self.turn_right(orientation)
        neighbors.append((loc, new_orientation, 'turnright', 2))

        return neighbors

    def turn_left(self, orientation):
        directions = ['N', 'W', 'S', 'E']
        idx = directions.index(orientation)
        return directions[(idx + 1) % 4]

    def turn_right(self, orientation):
        directions = ['N', 'E', 'S', 'W']
        idx = directions.index(orientation)
        return directions[(idx + 1) % 4]

    def get_path(self):
        return self.path
