
import random
import numpy as np
import queue
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
        if self.t < len(self.actions):
            action = self.actions[self.t]
            self.t += 1
        else:
            action = None
        # ------------------

        return action

    def find_path(self):
        # path = []
        # actions = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE

        actions = ['turnleft', 'turnright', 'forward']
        move_dir = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
        left_turn = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        right_turn = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        action_cost = {'turnleft': 5, 'turnright': 2, 'forward': 1}

        s = (self.loc[0], self.loc[1], self.dir)
        g = (self.goal[0], self.goal[1])
        nodes = [(x, y, d) for (x, y) in self.locations for d in ['N', 'E', 'S', 'W']]

        visited = set()
        inf = float('inf')
        cost = {n: inf for n in nodes}
        parent = {n: None for n in nodes}
        act_parent = {n: None for n in nodes}

        q = PriorityQueue()
        q.put((0, s))
        cost[s] = 0

        while not q.empty():
            _, cur_n = q.get()

            if cur_n in visited:
                continue
            visited.add(cur_n)

            (x, y, d) = cur_n
            if (x, y) == g:
                break

            for a in actions:
                if a == 'turnleft':
                    nh = (x, y, left_turn[d])
                    step_cost = action_cost[a]
                elif a == 'turnright':
                    nh = (x, y, right_turn[d])
                    step_cost = action_cost[a]
                else:
                    dx, dy = move_dir[d]
                    nx, ny = x + dx, y + dy
                    nh = (nx, ny, d)
                    step_cost = action_cost[a]
                    if (nx, ny) not in self.locations:
                        continue

                if nh in visited:
                    continue

                old_cost = cost[nh]
                new_cost = cost[cur_n] + step_cost

                if new_cost < old_cost:
                    cost[nh] = new_cost
                    parent[nh] = cur_n
                    act_parent[nh] = a
                    h = abs(nh[0] - g[0]) + abs(nh[1] - g[1])
                    priority = new_cost + h
                    q.put((priority, nh))

        goal_states = [(x, y, d) for (x, y, d) in cost.keys() if (x, y) == g]
        cur_n = min(goal_states, key=lambda st: cost[st]) if goal_states else s

        path = []
        actions_seq = []

        while cur_n is not None:
            path.append(cur_n)
            if act_parent[cur_n] is not None:
                actions_seq.append(act_parent[cur_n])
            cur_n = parent[cur_n]
        path.reverse()
        actions_seq.reverse()

        print(path)
        return path, actions_seq


    def get_path(self):
        return self.path
