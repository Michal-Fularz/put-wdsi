import random
import numpy as np
import queue
import math


class Agent:
    def __init__(self, size, walls, graph, loc, dir, goal):
        self.size = size
        self.walls = walls
        self.graph = graph
        # list of valid locations
        self.locations = list(self.graph.keys())
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal
        self.step = 0
        self.path = self.find_path()

    def __call__(self):
        action = self.path[self.step]
        self.step = self.step + 1

        return action

    def find_path(self):
        path = []

        s = self.loc
        nodes = list(self.graph.keys())
        visited = set()
        cost = {n: math.inf for n in nodes}
        parent = {n: None for n in nodes}

        q = queue.PriorityQueue()
        q.put((0, s))
        cost[s] = 0
        parent[s] = s

        while not q.empty():
            cur_n = q.get()[1]

            if cur_n in visited:
                continue
            visited.add(cur_n)

            if cur_n == self.goal:
                break

            for nh in self.graph[cur_n]:
                if nh in visited:
                    continue

                old_cost = cost[nh]

                x, y = cur_n
                x1, y1 = nh

                distance = math.sqrt((x - x1)**2 + (y - y1)**2)

                new_cost = cost[cur_n] + distance
                if new_cost < old_cost:
                    cost[nh] = new_cost
                    parent[nh] = cur_n
                    q.put((new_cost, nh))

        cur_n = self.goal
        while cur_n != s:
            path.append(cur_n)
            cur_n = parent[cur_n]
        path.append(s)
        path.reverse()

        print(path)
        return path

    def get_path(self):
        return self.path
