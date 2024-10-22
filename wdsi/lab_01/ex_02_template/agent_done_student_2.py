import random
import queue
import numpy as np
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
        self.path = self.find_path()

    def __call__(self):
        action = 'N'

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE
        if(self.path[self.t][0] > self.path[self.t+1][0]):
            action = 'W'
        elif(self.path[self.t][0] < self.path[self.t+1][0]):
            action = 'E'
        elif(self.path[self.t][1] > self.path[self.t+1][1]):
            action = 'S'
        elif(self.path[self.t][1] < self.path[self.t+1][1]):
            action = 'N'

        self.t = self.t + 1


        # ------------------

        return action

    def find_path(self):
        path = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE
        q = queue.Queue()

        current_f = self.loc
        q.put(current_f)

        visited = []
        visited.append(current_f)
        parent = {n: None for n in self.locations}

        while q:

            current_f = q.get()

            if(current_f == self.goal):
                break

            for i in range(4):
                if(i == 0):
                    x = current_f[0] + 1
                    nf = (x, current_f[1])
                elif(i == 1):
                    x = current_f[0] - 1
                    nf = (x, current_f[1])
                elif(i == 2):
                    y = current_f[1] + 1
                    nf = (current_f[0]), y
                elif(i == 3):
                    y = current_f[1] - 1
                    nf = (current_f[0]), y

                if nf not in visited and nf not in self.walls:
                    parent[nf] = current_f
                    q.put(nf)
                    visited.append(nf)
        current_f = self.goal
        while current_f != self.loc:
            path.append(current_f)
            current_f = parent[current_f]

        path.append(self.loc)
        path = list(reversed(path))


        # ------------------

        return path

    def get_path(self):
        return self.path