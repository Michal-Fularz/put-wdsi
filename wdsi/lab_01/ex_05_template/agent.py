# prob.py
# This is

import random
import numpy as np
import queue

from gridutil import *


class Agent:
    def __init__(self, size, walls, loc, dir, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
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



        # ------------------

        return action

    def find_path(self):
        path = []
        actions = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE

        

        # ------------------

        return path, actions

    def get_path(self):
        return self.path
