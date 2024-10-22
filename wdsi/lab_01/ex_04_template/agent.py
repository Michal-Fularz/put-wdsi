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

        self.path = self.find_path()

    def __call__(self):
        action = self.loc

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE



        # ------------------

        return action

    def find_path(self):
        path = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE

        

        # ------------------

        return path

    def get_path(self):
        return self.path
